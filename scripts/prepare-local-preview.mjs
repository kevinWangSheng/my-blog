import { copyFileSync, existsSync, mkdirSync, readlinkSync, rmSync, symlinkSync } from 'node:fs';
import { relative, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const dist = resolve(root, 'site/dist');
const serveDir = resolve(root, 'out/ui-serve');
const baseMount = resolve(serveDir, 'my-blog');
const rootIndex = resolve(serveDir, 'index.html');
const distIndex = resolve(dist, 'index.html');

if (!existsSync(distIndex)) {
  console.error('Missing site/dist/index.html. Run `pnpm --dir site build` first.');
  process.exit(1);
}

mkdirSync(serveDir, { recursive: true });

let needsLink = true;
if (existsSync(baseMount)) {
  try {
    const current = resolve(serveDir, readlinkSync(baseMount));
    needsLink = current !== dist;
  } catch {
    needsLink = true;
  }
  if (needsLink) rmSync(baseMount, { recursive: true, force: true });
}

if (needsLink) {
  symlinkSync(relative(serveDir, dist), baseMount, 'dir');
}

// Keep local root URL convenient while preserving the GitHub Pages base path.
// The copied HTML still points assets and internal links at /my-blog/.
copyFileSync(distIndex, rootIndex);

console.log(JSON.stringify({
  ok: true,
  serveDir,
  root: '/',
  base: '/my-blog/',
  rootIndex,
  baseMount,
}, null, 2));
