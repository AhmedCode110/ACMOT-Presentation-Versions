import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('/Users/ahmedgouda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { Presentation, PresentationFile } = await import('file:///Users/ahmedgouda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs');

const workspaceDir = '/Users/ahmedgouda/Desktop/ACMOT-Presentation-Versions';
const sourceDir = path.join(workspaceDir, 'versions/v49-fast-media-loading');
const buildDir = path.join(workspaceDir, '.pptx-build-v49');
const outputPath = path.join(workspaceDir, 'pptx_exports/AC-MOT-v49-Real-Time-Detection-and-Tracking.pptx');
const skillDir = '/Users/ahmedgouda/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.12148/skills/presentations';
const runtimePython = '/Users/ahmedgouda/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';

await fs.rm(buildDir, { recursive: true, force: true });
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(path.dirname(outputPath), { recursive: true });

const browser = await chromium.launch({ headless: true, executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(sourceDir, 'index.html')).href + '#1', { waitUntil: 'load' });
await page.waitForTimeout(1800);
const count = await page.locator('section.slide[data-sec]:not(.xpage)').count();
const pngs = [];
for (let i = 0; i < count; i++) {
  await page.evaluate(async (idx) => {
    const slides = [...document.querySelectorAll('section.slide[data-sec]:not(.xpage)')];
    slides.forEach((s, j) => { s.classList.toggle('active', j === idx); s.classList.toggle('past', j < idx); });
    document.body.classList.add('present');
    const s = slides[idx];
    s.querySelectorAll('[data-src]').forEach((m) => { m.src = m.getAttribute('data-src'); m.removeAttribute('data-src'); });
    if (window.ACMOT_FIT) window.ACMOT_FIT();
    s.querySelectorAll('[data-chart]').forEach((h) => {
      const fn = window.ACMOT_CHARTS && window.ACMOT_CHARTS[h.getAttribute('data-chart')];
      if (fn && !h.getAttribute('data-built')) { try { fn(h); h.setAttribute('data-built', '1'); } catch (_) {} }
      h.classList.add('play');
    });
  }, i);
  await page.waitForTimeout(280);
  const out = path.join(buildDir, `slide-${String(i + 1).padStart(3, '0')}.png`);
  await page.screenshot({ path: out, type: 'png' });
  pngs.push(out);
}
await browser.close();

const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
for (let i = 0; i < pngs.length; i++) {
  const slide = presentation.slides.add();
  slide.images.add({ blob: await fs.readFile(pngs[i]), contentType: 'image/png', position: { left: 0, top: 0, width: 1280, height: 720 }, fit: 'fill', alt: `AC-MOT presentation slide ${i + 1}` });
}

const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, 'container_tools/artifact_tool_utils.mjs')).href);
const stagingDir = path.join(buildDir, 'finalizer');
await fs.mkdir(stagingDir, { recursive: true });
const candidatePath = path.join(stagingDir, 'candidate.pptx');
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const result = await finalizePresentation({
  explicitTotalSlideCount: count,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  workspaceDir,
  candidatePath,
  finalPath: outputPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000'],
  requiredNativeTableOwnerSlides: [],
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, 'AC-MOT-v49-Real-Time-Detection-and-Tracking.validation.json'),
});
console.log(JSON.stringify({ outputPath, slideCount: count, result }, null, 2));
