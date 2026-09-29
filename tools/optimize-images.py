#!/usr/bin/env python3
"""Gera as imagens otimizadas da landing page a partir dos arquivos originais.

Uso (na raiz do projeto):
    python3 tools/optimize-images.py

Requer Pillow (pip install pillow) e a pasta materiais-de-origem/. Os
originais nunca são alterados. Para trocar uma foto, substitua o arquivo de
origem ou edite a lista PHOTOS e rode o script novamente.
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "materiais-de-origem"
SRC = SOURCES / "fotos"
LOGO_SRC = SOURCES / "logo" / "logo-amigos.png"
PARTS_SRC = ROOT / "tools" / "parts"
OUT = ROOT / "assets" / "img"

NAVY = (3, 25, 75)          # #03194B, fundo do logo e fundo escuro da página
LOGO_WHITE = (245, 250, 255)
LOGO_RED = (192, 9, 25)     # #C00919

# nome de saída -> (arquivo em materiais-de-origem/fotos, área usada)
# As fotos recebidas têm 382x510 px. Nada é ampliado. A área é (esquerda,
# topo, direita, base) em pixels do original, ou None para a foto inteira.
PHOTOS = {
    "fachada": ("004.webp", (0, 96, 382, 430)),
    "balcao-e-calotas": ("005.webp", None),
    "balcao-de-atendimento": ("003.webp", None),
    "prateleira-de-oleos": ("002.webp", None),
    "tambores-de-freio": ("006.webp", None),
}


def build_photos() -> None:
    for name, (source, area) in PHOTOS.items():
        im = Image.open(SRC / source).convert("RGB")
        if area:
            im = im.crop(area)
        im.save(OUT / f"{name}-{im.width}.webp", "WEBP", quality=84, method=6)
        # fallback JPEG para navegadores sem WebP
        im.save(OUT / f"{name}-{im.width}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
        print(f"{name}: {im.width}x{im.height}")


def extract_logo(logo: Image.Image) -> Image.Image:
    """Separa o logo do fundo azul.

    O arquivo recebido é uma captura de tela: carro em traço branco, "AMIGOS"
    em vermelho e "AUTO PEÇAS" em branco, sobre um azul que escurece para as
    bordas. O azul quase não tem vermelho (canal R perto de zero), então a
    quantidade de branco e de vermelho de cada pixel pode ser medida pelos
    canais. O resultado tem as cores originais e fundo transparente. Nada é
    redesenhado."""
    rgb = logo.convert("RGB")
    width, height = rgb.size
    out = Image.new("RGBA", rgb.size)
    source, target = rgb.load(), out.load()
    for y in range(height):
        # o verde do fundo vai de 15 (topo) a 33 (base)
        green_bg = 15 + 18 * y / height
        for x in range(width):
            r, g, b = source[x, y]
            white = max(0.0, min(1.0, (g - green_bg - 6) / (LOGO_WHITE[1] - green_bg - 6)))
            red = max(0.0, min(1.0, (r - LOGO_WHITE[0] * white - 6) / (LOGO_RED[0] - 6)))
            alpha = min(1.0, white + red)
            if alpha < 0.06:
                target[x, y] = (0, 0, 0, 0)
                continue
            total = white + red
            color = tuple(
                round((LOGO_WHITE[i] * white + LOGO_RED[i] * red) / total) for i in range(3)
            )
            target[x, y] = color + (round(alpha * 255),)
    return out


def build_logo() -> None:
    logo = Image.open(LOGO_SRC)
    # amplia antes de separar, para as bordas ficarem suaves
    big = logo.convert("RGB").resize((logo.width * 2, logo.height * 2), Image.LANCZOS)
    mark = extract_logo(big)
    box = mark.getchannel("A").point(lambda v: 255 if v > 60 else 0).getbbox()
    margin = 8
    mark = mark.crop((
        max(0, box[0] - margin), max(0, box[1] - margin),
        min(mark.width, box[2] + margin), min(mark.height, box[3] + margin),
    ))
    mark.save(OUT / "logo-amigos-auto-pecas.png", optimize=True)
    mark.save(OUT / "logo-amigos-auto-pecas.webp", "WEBP", quality=94, method=6)
    print(f"logo-amigos-auto-pecas: {mark.width}x{mark.height}")

    # Ícones: o logo sobre o azul da marca
    for name, size in (("favicon-32", 32), ("apple-touch-icon", 180), ("icon-192", 192)):
        tile = Image.new("RGB", (512, 512), NAVY)
        fitted = mark.resize((452, round(mark.height * 452 / mark.width)), Image.LANCZOS)
        tile.paste(fitted, ((512 - fitted.width) // 2, (512 - fitted.height) // 2), fitted)
        tile.resize((size, size), Image.LANCZOS).save(OUT / f"{name}.png", optimize=True)


def build_parts() -> None:
    """Converte as peças ilustrativas geradas por tools/render-parts.py e
    tools/render-parts.js. Se os PNG não existirem, mantém o que já está em
    assets/img."""
    sources = sorted(PARTS_SRC.glob("peca-*.png"))
    if not sources:
        print("peças: PNG não encontrados em tools/parts, etapa ignorada")
        return
    for source in sources:
        im = Image.open(source)
        if "sem-fundo" in source.stem:
            im = im.convert("RGBA")
            im = im.crop(im.getchannel("A").getbbox())
            for width in (360, 720):
                height = round(im.height * width / im.width)
                im.resize((width, height), Image.LANCZOS).save(
                    OUT / f"{source.stem}-{width}.webp", "WEBP", quality=86, method=6
                )
            height = round(im.height * 720 / im.width)
            im.resize((720, height), Image.LANCZOS).save(OUT / f"{source.stem}-720.png", optimize=True)
            print(f"{source.stem}: {im.width}x{im.height}")
            continue
        im = im.convert("RGB")
        for width in (480, 900):
            height = round(im.height * width / im.width)
            im.resize((width, height), Image.LANCZOS).save(
                OUT / f"{source.stem}-{width}.webp", "WEBP", quality=84, method=6
            )
        im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(
            OUT / f"{source.stem}-900.jpg", "JPEG", quality=84, optimize=True, progressive=True
        )
        print(f"{source.stem}: {im.width}x{im.height}")


def build_social_card() -> None:
    """Imagem de compartilhamento (1200x630): logo à esquerda e peça à direita."""
    card = Image.new("RGB", (1200, 630), NAVY)

    logo = Image.open(OUT / "logo-amigos-auto-pecas.png").convert("RGBA")
    logo = logo.resize((560, round(logo.height * 560 / logo.width)), Image.LANCZOS)
    card.paste(logo, (70, (630 - logo.height) // 2), logo)

    disc = OUT / "peca-disco-de-freio-sem-fundo-720.png"
    if disc.exists():
        part = Image.open(disc).convert("RGBA")
        part = part.resize((520, round(part.height * 520 / part.width)), Image.LANCZOS)
        card.paste(part, (660, (630 - part.height) // 2), part)

    card.save(OUT / "compartilhamento.jpg", "JPEG", quality=88, optimize=True, progressive=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_photos()
    build_logo()
    build_parts()
    build_social_card()
    total = sum(f.stat().st_size for f in OUT.iterdir())
    print(f"{len(list(OUT.iterdir()))} arquivos, {total / 1024:.0f} KB no total")
