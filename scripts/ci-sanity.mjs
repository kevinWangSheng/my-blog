#!/usr/bin/env node
import { existsSync } from 'node:fs';
import { readdir, readFile } from 'node:fs/promises';
import { join, relative, resolve } from 'node:path';

const root = resolve(new URL('..', import.meta.url).pathname);
const dist = join(root, 'site/dist');
const errors = [];
const warnings = [];

const fail = (message) => errors.push(message);
const warn = (message) => warnings.push(message);

async function walk(dir) {
  if (!existsSync(dir)) return [];
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile()) files.push(full);
  }
  return files;
}

async function readMaybe(path) {
  if (!existsSync(path)) return '';
  return readFile(path, 'utf8');
}

function rel(path) {
  return relative(root, path);
}

for (const legacyPath of ['.gitmodules', 'config.yaml', 'assets', 'content', 'themes', 'resources', 'public', 'archetypes', '.hugo_build.lock', 'hugo_blog_setup_plan.md', 'scripts/notion-sync.py']) {
  if (existsSync(join(root, legacyPath))) fail(`legacy Hugo/Notion path must not exist: ${legacyPath}`);
}

if (!existsSync(join(root, 'site/package.json'))) fail('missing Astro site/package.json');
if (!existsSync(join(dist, 'index.html'))) fail('missing site/dist/index.html; run pnpm --dir site build first');

const workflowFiles = await walk(join(root, '.github/workflows'));
for (const file of workflowFiles) {
  const text = await readFile(file, 'utf8');
  if (/(notion|hugo|themes\/|content\/posts|public\/)/i.test(text)) fail(`workflow references legacy pipeline: ${rel(file)}`);
  if (/(content:sync|content-sync|content-sync\.mjs|blog-publisher|kb-vault|docs\/content-pipeline\/manifests)/i.test(text)) {
    fail(`workflow attempts content publishing/sync instead of build-only CI/CD: ${rel(file)}`);
  }
}

const rss = await readMaybe(join(dist, 'rss.xml'));
const sitemap = await readMaybe(join(dist, 'sitemap.xml'));
if (!rss.includes('<rss')) fail('rss.xml was not generated');
if (!sitemap.includes('<urlset')) fail('sitemap.xml was not generated');
if (!sitemap.includes('/my-blog/logs/')) fail('sitemap.xml should include the empty Logs section route');

const distFiles = await walk(dist);
const htmlXmlFiles = distFiles.filter((file) => /\.(html|xml|txt|json|js|css)$/i.test(file));
const forbiddenPublicPatterns = [
  [/\/Users\/shenghuikevin/i, 'local absolute user path'],
  [/kb-vault/i, 'private KB vault path'],
  [/docs\/content-pipeline/i, 'internal content pipeline path'],
  [/private draft|confidential|禁止发布|do not publish/i, 'private/forbidden publish marker'],
  [/Blog rebuild|Week 24|2026-blog-rebuild|2026-week-24/i, 'old build-test log content'],
  [/Astro Content Collections|axe-core|\/axe-core|Playwright<\/h|Lighthouse<\/h/i, 'old build-tool source shelf entry']
];

for (const file of htmlXmlFiles) {
  const text = await readFile(file, 'utf8');
  for (const [pattern, label] of forbiddenPublicPatterns) {
    if (pattern.test(text)) fail(`${label} leaked into public output: ${rel(file)}`);
  }
}

if (existsSync(join(dist, 'logs/_type-anchor/index.html'))) fail('draft Logs type anchor was publicly generated');
if (existsSync(join(dist, 'logs/2026-blog-rebuild-t13/index.html'))) fail('old build log route was generated');
if (existsSync(join(dist, 'logs/2026-week-24/index.html'))) fail('old weekly build log route was generated');

const contentFiles = await walk(join(root, 'site/src/content'));
for (const file of contentFiles) {
  const text = await readFile(file, 'utf8');
  if (/visibility:\s*(private|draft)/i.test(text)) {
    const slug = file.replace(/^.*\/src\/content\//, '').replace(/\.(md|mdx)$/i, '');
    const outputPath = join(dist, slug, 'index.html');
    if (existsSync(outputPath)) fail(`draft/private content generated publicly: ${rel(file)} -> ${rel(outputPath)}`);
  }
}

if (!existsSync(join(dist, 'logs/index.html'))) fail('empty Logs section route should be generated at site/dist/logs/index.html');
else {
  const logsIndex = await readFile(join(dist, 'logs/index.html'), 'utf8');
  if (!logsIndex.includes('这个集合暂时为空')) warn('Logs page does not contain the standard empty collection message');
}

const summary = { ok: errors.length === 0, errors, warnings };
console.log(JSON.stringify(summary, null, 2));
process.exit(summary.ok ? 0 : 1);
