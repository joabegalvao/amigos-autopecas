#!/usr/bin/env node
/* Converte os SVG de tools/parts/ em imagens PNG, abrindo cada um no Chromium.

   Uso (na raiz do projeto), depois de rodar tools/render-parts.py:
       node tools/render-parts.js

   Requer Playwright. Informe o caminho do módulo e do navegador pelas
   variáveis PLAYWRIGHT_MODULE e CHROMIUM_PATH, se não estiverem no padrão.
   Os PNG ficam em tools/parts/ e são convertidos para WebP e JPEG por
   tools/optimize-images.py. Arquivos com "sem-fundo" no nome saem com fundo
   transparente. */

const fs = require('fs');
const path = require('path');

const modulePath = process.env.PLAYWRIGHT_MODULE || 'playwright';
const { chromium } = require(modulePath);

const dir = path.join(__dirname, 'parts');

(async () => {
  const browser = await chromium.launch(
    process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}
  );
  const page = await browser.newPage({ viewport: { width: 900, height: 640 }, deviceScaleFactor: 2 });

  for (const file of fs.readdirSync(dir).filter((name) => name.endsWith('.svg')).sort()) {
    await page.goto('file://' + path.join(dir, file));
    await page.waitForTimeout(150);
    const out = path.join(dir, file.replace('.svg', '.png'));
    await page.screenshot({ path: out, omitBackground: file.includes('sem-fundo') });
    console.log(path.basename(out));
  }

  await browser.close();
})().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
