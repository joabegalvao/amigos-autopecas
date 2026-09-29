# Amigos Auto Peças | Landing page

Página única, estática, em HTML, CSS e JavaScript puro. Não há etapa de build
nem dependências de execução: basta servir a pasta.

## Como visualizar

```bash
# na raiz do projeto
python3 -m http.server 4181
# abra http://localhost:4181
```

Qualquer servidor estático funciona (Nginx, Apache, Netlify, Vercel, Hostinger).
Publique `index.html` e a pasta `assets/`. A pasta `tools/` não precisa ir para
o servidor.

### Materiais de origem

Os arquivos enviados pelo cliente ficam reunidos na pasta
`materiais-de-origem/`, que não faz parte do repositório: ela existe só na
pasta local do projeto e é ignorada pelo git. As imagens que o site usa já
estão prontas em `assets/img`.

```
materiais-de-origem/
  logo/          logo-amigos.png
  fotos/         sete fotos da loja (001 a 007)
```

Só é preciso ter os originais para rodar `tools/optimize-images.py`, ou seja,
para trocar ou reprocessar uma foto.

| Arquivo de origem | Conteúdo | Usado em |
| --- | --- | --- |
| `logo/logo-amigos.png` | Captura de tela do logo, 332 x 161 px | cabeçalho, rodapé, ícones e imagem de compartilhamento |
| `fotos/004.webp` | Fachada, de frente | hero (recortada) |
| `fotos/005.webp` | Balcão e parede de calotas | a loja |
| `fotos/003.webp` | Balcão com clientes | a loja |
| `fotos/002.webp` | Prateleira de óleos | a loja |
| `fotos/006.webp` | Tambores de freio no salão | a loja |
| `fotos/001.webp`, `fotos/007.webp` | Fachada, outros ângulos | não usadas |

As fotos 004 e 006 não vieram na pasta. Foram baixadas do site atual da loja,
que é a origem das outras cinco.

## Repositório

| Item | Valor |
| --- | --- |
| Endereço | `git@github.com:joabegalvao/amigos-autopecas.git` |
| Página | https://github.com/joabegalvao/amigos-autopecas |
| Visibilidade | pública (conferida em 29/09/2026) |
| Branch | `main` |

O repositório guarda só o que o site precisa para funcionar e ser mantido:
`index.html`, `assets/`, `tools/`, `README.md` e `.gitignore`.

```bash
git clone git@github.com:joabegalvao/amigos-autopecas.git
```

Um clone novo abre e publica o site normalmente. Só não roda o script de
imagens, que depende da pasta `materiais-de-origem/`.

## Dados do cliente

Recebidos em 29/09/2026.

### Informados no briefing

| Dado | Valor |
| --- | --- |
| Nome | Amigos Auto Peças |
| Segmento | Peças automotivas |
| Veículos atendidos | Carros, furgões, camionetas e caminhões |
| Tradição | Mais de 25 anos no mercado automotivo |
| Diferenciais | Peças originais e compatíveis, atendimento especializado, preços competitivos, localização privilegiada |
| Números | 70.000+ clientes satisfeitos, 5.000+ peças em estoque |
| WhatsApp | (44) 99816-0010 |
| Telefone | (44) 3262-4144 |
| Instagram | https://www.instagram.com/autopecas.amigos/ |
| Endereço | Praça José de Bonifácio, 304 |

Listas de peças por veículo, como vieram no briefing:

| Carros | Caminhões | Furgões e camionetas |
| --- | --- | --- |
| Motor e transmissão | Peças de motor diesel | Peças de motor |
| Suspensão e freios | Sistema de freios | Sistema de direção |
| Sistema elétrico | Suspensão pesada | Peças de câmbio |
| Acessórios diversos | Peças de carroceria | Acessórios comerciais |

### Tirados do site atual da loja

O site atual (https://yvhbatmz.manus.space/) foi indicado como referência. De
lá vieram dados que não estavam no briefing:

| Dado | Valor |
| --- | --- |
| Horário | Segunda a sexta, 8h às 18h. Sábado, 8h às 15h. Domingo e feriado, 9h às 12h |
| E-mail | autopecasamigos@hotmail.com |
| Bairro e CEP | Zona 01, CEP 87013-290 |
| Mercado Livre | https://www.mercadolivre.com.br/pagina/autopecasamigos |

### Lidos na foto da fachada

O letreiro da loja traz oito marcas: Fiat, Ford, GM, VW, Perkins, MWM,
Mercedes e Willys. A página cita as marcas em texto, como aparecem no
letreiro, sem usar logotipos.

### Divergência encontrada: nota no Google

O briefing diz "nota 5 no Google". Em 29/09/2026, o perfil "Auto Peças
Amigos", no endereço da loja, mostrava **nota 3,9 com 149 avaliações**.

Por isso:

- a página **não cita** nota nem avaliações;
- o mapa é carregado pelo endereço, e não pelo nome da loja. Assim o Google
  mostra só o endereço, sem o cartão com a nota.

### Público-alvo

O briefing traz "mulheres" como público-alvo, o mesmo do projeto anterior
(nail designer). Foi tratado como sobra do modelo. Os textos falam com quem
tem, conserta ou trabalha com veículo, sem marca de gênero.

## Estratégia

| Definição | Decisão |
| --- | --- |
| Proposta de valor | Um só balcão para a peça certa, do carro de passeio ao caminhão, com mais de 25 anos de experiência |
| Principal objeção | "Será que tem a peça do meu veículo? E como eu explico o que preciso?" |
| Conversão prioritária | Pedido de orçamento pelo WhatsApp |
| Ação secundária | Ligar para a loja |

## Seções da página

| Ordem | Seção | Âncora | Conteúdo |
| --- | --- | --- | --- |
| 1 | Cabeçalho | | Logo, navegação e CTA de orçamento. Fixo no topo |
| 2 | Hero | `#inicio` | "Peça certa, do carro ao caminhão", WhatsApp, telefone, foto da fachada e três números |
| 3 | Veículos | `#veiculos` | Carros, furgões e camionetas, caminhões, com as listas do briefing |
| 4 | Peças | `#pecas` | Seis sistemas ilustrados, cada um com link para o WhatsApp |
| 5 | A loja | `#a-loja` | Diferenciais, marcas do letreiro e quatro fotos |
| 6 | Como pedir | `#como-pedir` | Três passos |
| 7 | Onde fica | `#onde-fica` | Endereço, WhatsApp, telefone, horário e mapa |
| 8 | Chamada final | | WhatsApp e telefone |
| 9 | Rodapé | | Endereço, contato, Instagram e Mercado Livre |

Componente de apoio: botão flutuante de WhatsApp, no canto inferior direito,
em todas as telas.

Não há seção de avaliações, porque nenhuma foi enviada.

### O que mudou em relação ao site atual

| Site atual | Esta página |
| --- | --- |
| Primeira tela quase vazia, com o conteúdo abaixo da dobra | Proposta, botões e foto da loja na primeira tela |
| Rolagem lateral no celular (página de 425 px em tela de 390) | Sem rolagem lateral de 320 a 1920 px |
| Contador de "visitantes hoje" | Removido |
| Números animados, que mostram valores errados enquanto contam | Números fixos |
| Formulário de contato sem destino conhecido | Sem formulário. Contato por WhatsApp e telefone |
| Um WhatsApp genérico | Dez mensagens prontas, por veículo e por sistema |
| Ícone de carro no lugar de imagens | Foto da fachada e seis peças ilustradas |

## Estrutura de arquivos

```
index.html                 conteúdo e SEO
assets/css/styles.css      estilos (tokens de cor e tipografia no topo)
assets/js/main.js          menu e revelação na rolagem
assets/img/                imagens otimizadas (geradas pelos scripts)
assets/fonts/              Kanit e Public Sans (arquivos locais)
tools/optimize-images.py   gera assets/img a partir dos originais
tools/render-parts.py      desenha as seis peças ilustrativas, em SVG
tools/render-parts.js      transforma os SVG em imagem, pelo Chromium
tools/parts/               SVG das peças (os PNG intermediários ficam fora do git)
materiais-de-origem/       arquivos do cliente (só na pasta local, fora do git)
```

## Como atualizar o conteúdo

| O que mudar | Onde |
| --- | --- |
| Textos e endereço | `index.html` (seções comentadas) |
| Número e mensagem do WhatsApp | `index.html`: procure por `wa.me/` (16 ocorrências). O texto vem depois de `?text=`, com espaços escritos como `%20` e acentos codificados |
| Telefone | `index.html`: procure por `tel:` (4 ocorrências) e o bloco JSON-LD no `<head>` |
| Horário | `index.html`: seção "ONDE FICA" e bloco JSON-LD |
| Números do hero | `index.html`, lista `facts` |
| Listas de peças por veículo | `index.html`, blocos `<article class="vehicle">` |
| Sistemas (texto e link) | `index.html`, lista `parts__grid` |
| Sistemas (desenho e cor) | `tools/render-parts.py`. Depois rode os três comandos abaixo |
| Marcas do letreiro | `index.html`, bloco `brands` |
| Mapa | `index.html`: procure por `google.com/maps` (3 ocorrências, uma delas no `<iframe>`) |
| Cores e fontes | `assets/css/styles.css`, bloco `:root` |
| Fotos | substitua o original, ajuste a lista `PHOTOS` em `tools/optimize-images.py` e rode o script |

Mensagens de WhatsApp, conforme o ponto da página:

| Onde | Mensagem |
| --- | --- |
| Cabeçalho, hero, "Como pedir", "Onde fica", chamada final, rodapé e botão flutuante | Olá! Vi o site da Amigos Auto Peças e quero um orçamento. |
| Veículos | ... quero cotar uma peça para carro / para furgão ou camioneta / para caminhão. |
| Peças | ... quero cotar peças de motor / de câmbio e transmissão / de suspensão / de freio / do sistema elétrico / acessórios. |

Para gerar as imagens (requer Pillow e a pasta `materiais-de-origem/`):

```bash
python3 tools/optimize-images.py
```

Para redesenhar as peças ilustrativas (requer Node e Playwright):

```bash
python3 tools/render-parts.py      # escreve os SVG em tools/parts
node tools/render-parts.js         # transforma cada SVG em PNG
python3 tools/optimize-images.py   # converte para WebP e JPEG em assets/img
```

Se o Playwright não estiver instalado no projeto, informe os caminhos pelas
variáveis `PLAYWRIGHT_MODULE` e `CHROMIUM_PATH`. Sem os PNG, o
`optimize-images.py` mantém as peças que já estão em `assets/img`.

### Título do hero

O tamanho da letra é calculado para que as linhas caibam na coluna. No celular
o título tem três linhas e, a partir de 600 px, duas. Se o texto mudar,
confira a quebra em 320, 600 e 900 px de largura. A regra está em
`.hero__title`, no `styles.css`.

### Cache do navegador

Os arquivos de estilo e script são chamados com versão: `styles.css?v=1` e
`main.js?v=1`. Ao alterar um deles, aumente o número no `index.html` para que
os visitantes recebam a versão nova.

## Identidade visual

| Token | Cor | Origem |
| --- | --- | --- |
| `--navy` | `#03194B` | fundo do logo |
| `--red` | `#C00919` | "AMIGOS", no logo |
| `--white` | `#FFFFFF` | carro e "AUTO PEÇAS", no logo |
| `--navy-900`, `--navy-line` | `#020F30`, `#1B3172` | azul mais fechado e linhas sobre o azul |
| `--red-300` | `#FF6470` | vermelho clareado, para destaques sobre o azul |
| `--red-700` | `#9C0613` | vermelho escurecido, para o botão ao passar o mouse |
| `--mist`, `--line` | `#EEF1F5`, `#D6DCE7` | fundo das imagens de peças, seções claras e linhas |
| `--ink`, `--ink-soft`, `--navy-soft` | `#0C1530`, `#4A5470`, `#B4C0DD` | textos |
| `--whatsapp` | `#25D366` | verde oficial do WhatsApp, usado só no botão flutuante |

Azul, vermelho e branco são também as cores da fachada da loja.

Tipografia: Kanit (títulos, com itálico nos destaques) e Public Sans (textos).
O itálico pesado da Kanit é parente das letras de "AMIGOS" no logo.

Elementos que vêm da marca:

- Duas faixas inclinadas antes dos rótulos de seção, no ângulo das letras do
  logo.
- Destaques dos títulos em itálico.
- Filete vermelho deslocado atrás da foto da fachada.

O vermelho puro do logo não tem contraste suficiente sobre o azul. Por isso os
destaques sobre fundo azul usam a versão clareada.

### Peças ilustrativas

As seis imagens (pistão, engrenagens, amortecedor, disco de freio, bateria e
calota) foram criadas para este projeto. Elas são desenhadas por código
(`tools/render-parts.py`), com metal, brilho e sombra, e depois transformadas
em imagem. **Não são fotos e não mostram produtos do estoque.** A página diz
isso logo abaixo dos cartões, e os textos alternativos as identificam como
ilustração.

O disco de freio aparece também no hero, sobre a foto da fachada, e na imagem
de compartilhamento.

### Tratamento do logo

O arquivo recebido é uma captura de tela, com 332 x 161 px: o logo sobre um
azul que escurece para as bordas. Nada foi redesenhado. O script amplia a
imagem, separa o branco e o vermelho do fundo azul e salva o logo com fundo
transparente, nas cores originais.

O logo só aparece sobre o azul da marca (cabeçalho e rodapé). Sobre fundo
claro, o carro e "AUTO PEÇAS" somem, porque são brancos.

### Tratamento das fotos

As fotos recebidas têm 382 x 510 px. É pouco: em telas de alta densidade elas
ficam suaves. A página foi desenhada para isso:

- nenhuma foto é exibida com mais de 382 px de largura;
- as imagens grandes e nítidas da página são as peças ilustradas.

A foto da fachada foi recortada para tirar a rua e deixar o letreiro em
destaque.

## Decisões de conteúdo

- Os fatos da página vêm do briefing, do site atual da loja e da foto da
  fachada, listados acima. Não há preços, garantias ou promessas inventadas.
- "Marca própria" foi entendida como a marca Amigos Auto Peças.
- "70.000+ clientes satisfeitos" foi publicado como "70 mil+ clientes
  atendidos". Número de clientes é verificável. Satisfação, não.
- A nota do Google não aparece na página (veja "Divergência encontrada").
- "No centro de Maringá" corresponde à Zona 01, que é o centro da cidade.
- Os textos sobre o estoque à vista (calotas, grades, óleos, tambores de
  freio) descrevem o que as fotos mostram. "Calotas, volantes e mais", no
  cartão de acessórios, também.
- Os três passos de "Como pedir" descrevem um caminho de atendimento. A página
  não promete prazo de resposta nem entrega. O último passo é retirar na loja.
- O link do Mercado Livre foi publicado sem os parâmetros de pré-visualização
  que estavam no site atual.
- Não há formulário, porque não existe destino de envio definido.
- A foto do hero não tem legenda.
- O ícone do botão flutuante é escuro sobre o verde, e não branco, para manter
  contraste suficiente.

## Testes realizados

Executados em 29/09/2026, em Chromium automatizado (Playwright).

- Revisão visual das capturas de tela: página inteira em 390 e 1440 px.
- Sem rolagem horizontal nos tamanhos 320, 360, 390, 480, 599, 600, 768, 820,
  900, 1024, 1200, 1440 e 1920 px.
- Sem erros de console e sem imagens quebradas.
- 42 verificações automáticas aprovadas: menu no celular (toque, Esc, toque
  fora, foco), âncoras, botão flutuante de WhatsApp (posição, nome acessível,
  sem cobrir o texto do rodapé), fotos sem ampliação acima do tamanho real,
  mapa com título e carregamento adiado, revelação na rolagem, link de pular
  para o conteúdo, foco visível, destino e atributos de todos os links, dez
  mensagens de WhatsApp, hierarquia de títulos e atributos das imagens.
- O mapa foi aberto no teste e mostrou o marcador na Praça José de Bonifácio,
  304, Zona 01, sem cartão de avaliações.
- Página utilizável sem JavaScript.
- Animações desligadas quando o sistema pede movimento reduzido.
- Contraste AA em todos os textos (mínimo de 5,63:1).
- Carga inicial no celular de 314 KB, medida em tela de densidade 3x, sem
  saltos de layout (CLS 0). Página inteira: 534 KB, sem contar o mapa.
- O mapa do Google soma cerca de 1,8 MB, baixados só quando o visitante chega
  à seção "Onde fica".

Não testado: Safari, Firefox e aparelhos físicos. Dos links externos, foi
conferido apenas o endereço, não o conteúdo de destino. O Mercado Livre pede
verificação contra acesso automatizado, então a página da loja não pôde ser
aberta no teste. Também não foi verificado se o número responde no WhatsApp.

## Histórico de ajustes

| Ajuste | Arquivos |
| --- | --- |
| Versão inicial da página | todos |

## Créditos e licenças

- Logo e fotos da loja: fornecidos pelo cliente.
- Peças ilustrativas e ícones: criados para este projeto. Ícone do WhatsApp:
  Simple Icons (CC0).
- Kanit e Public Sans: SIL Open Font License 1.1, obtidas do Google Fonts e
  hospedadas localmente.
- Mapa: Google Maps, incorporado.

## Pendências que dependem do cliente

- **Nota do Google.** Esclarecer a diferença entre a "nota 5" do briefing e a
  nota 3,9 do perfil. Se houver outro perfil, enviar o link.
- **Números.** Confirmar "mais de 70 mil clientes" e "mais de 5 mil peças em
  estoque".
- **Horário.** Confirmar o horário tirado do site atual, em especial o de
  domingo e feriado.
- **Fotos em alta resolução**, da fachada, do balcão e de peças reais. As
  atuais têm 382 px de largura. Com fotos de produto, as ilustrações podem ser
  trocadas.
- Logo em arquivo digital, de preferência em vetor (SVG, AI ou PDF). O arquivo
  recebido é uma captura de tela.
- Confirmar as oito marcas do letreiro e dizer se há outras.
- Confirmar o endereço da loja no Mercado Livre.
- Informar se a loja faz entrega. Em caso positivo, a página pode dizer isso.
- Avaliações de clientes, com autorização de uso do nome.
- Autorização de uso de imagem das pessoas que aparecem nas fotos do balcão.
- Domínio de publicação, para completar `og:image` com URL absoluta e adicionar
  `link rel="canonical"`.
