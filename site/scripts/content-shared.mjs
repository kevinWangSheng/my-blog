import { readFile, readdir, mkdir, writeFile, copyFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { basename, dirname, extname, join, relative, resolve } from 'node:path';

export const COLLECTIONS = new Set(['projects', 'notes', 'logs', 'essays', 'links']);
export const REQUIRED = {
  projects: ['title', 'description', 'date', 'status', 'role', 'period'],
  notes: ['title', 'description', 'date', 'topic'],
  logs: ['title', 'description', 'date', 'period', 'summary'],
  essays: ['title', 'description', 'date'],
  links: ['title', 'description', 'date', 'url', 'category', 'note']
};
const SECRET_RE = /(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|PRIVATE) KEY|notion[_-]?token|api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,})/i;
const FORBIDDEN_RE = /(do\s*not\s*publish|不发布|禁止发布|private draft|confidential|机密)/i;

export function parseArgs(argv = process.argv.slice(2)) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else args[key] = next, i++;
  }
  return args;
}

export function slugify(input) {
  return String(input || '')
    .trim()
    .toLowerCase()
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\u4e00-\u9fff]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 90) || 'untitled';
}

export function isSafeSlug(slug) {
  return /^[a-z0-9\u4e00-\u9fff][a-z0-9\u4e00-\u9fff-]{0,89}$/.test(slug) && !slug.includes('..') && !slug.includes('/');
}

export function parseFrontmatter(raw) {
  if (!raw.startsWith('---\n')) return { data: {}, body: raw, hasFrontmatter: false };
  const end = raw.indexOf('\n---', 4);
  if (end === -1) return { data: {}, body: raw, hasFrontmatter: false };
  const block = raw.slice(4, end).trim();
  const body = raw.slice(raw.indexOf('\n', end + 1) + 1);
  const data = {};
  let currentKey = null;
  for (const line of block.split(/\r?\n/)) {
    if (!line.trim()) continue;
    const list = line.match(/^\s+-\s+(.+)$/);
    if (list && currentKey) {
      data[currentKey] ??= [];
      if (Array.isArray(data[currentKey])) data[currentKey].push(coerceScalar(list[1]));
      continue;
    }
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    const [, key, value] = m;
    currentKey = key;
    data[key] = value === '' ? [] : coerceScalar(value);
  }
  return { data, body, hasFrontmatter: true };
}

function coerceScalar(value) {
  const trimmed = String(value).trim();
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    return trimmed.slice(1, -1).split(',').map((x) => stripQuotes(x.trim())).filter(Boolean);
  }
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  return stripQuotes(trimmed);
}

function stripQuotes(value) {
  return value.replace(/^['\"]|['\"]$/g, '');
}

export function toFrontmatter(data) {
  const lines = ['---'];
  for (const [key, value] of Object.entries(data)) {
    if (value == null) continue;
    if (Array.isArray(value)) lines.push(`${key}: [${value.map((v) => JSON.stringify(String(v))).join(', ')}]`);
    else lines.push(`${key}: ${JSON.stringify(String(value))}`);
  }
  lines.push('---', '');
  return lines.join('\n');
}

function safeJoin(root, child) {
  const full = resolve(root, child);
  const rel = relative(resolve(root), full);
  if (rel.startsWith('..') || rel === '' || rel.includes('..')) throw new Error(`unsafe path: ${child}`);
  return full;
}

export async function loadItems(args) {
  if (args.file) {
    const file = resolve(args.file);
    const type = args.type;
    return [{ file, type, slug: args.slug, sourceRoot: dirname(file) }];
  }
  const inputDir = args.input || args.dir;
  if (!inputDir) throw new Error('需要 --file <markdown> --type <collection> 或 --input <dir>');
  const root = resolve(inputDir);
  const manifestPath = join(root, 'manifest.json');
  if (!existsSync(manifestPath)) throw new Error(`manifest.json 不存在: ${manifestPath}`);
  const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
  const items = Array.isArray(manifest) ? manifest : manifest.items;
  if (!Array.isArray(items) || items.length === 0) throw new Error('manifest.json 需要包含非空 items 数组');
  return items.map((item, index) => {
    if (!item.file) throw new Error(`manifest item ${index} 缺 file`);
    return { ...item, file: safeJoin(root, item.file), sourceRoot: root };
  });
}

export async function readMarkdownItem(item) {
  if (!COLLECTIONS.has(item.type)) throw new Error(`未知 type: ${item.type}`);
  if (!['.md', '.mdx'].includes(extname(item.file))) throw new Error(`只支持 Markdown: ${item.file}`);
  const raw = await readFile(item.file, 'utf8');
  const parsed = parseFrontmatter(raw);
  const data = { ...parsed.data };
  data.tags ??= [];
  data.visibility ??= item.visibility ?? 'public';
  const slug = item.slug || data.slug || slugify(basename(item.file, extname(item.file)) || data.title);
  return { ...item, raw, ...parsed, data, slug };
}

export function getSiteRoot() {
  if (existsSync(resolve('src/content')) && existsSync(resolve('package.json'))) return resolve('.');
  if (existsSync(resolve('site/src/content'))) return resolve('site');
  return resolve('.');
}

export async function listExistingSlugs(siteRoot = getSiteRoot()) {
  const result = new Map();
  for (const collection of COLLECTIONS) {
    const dir = join(siteRoot, 'src/content', collection);
    const slugs = new Set();
    if (existsSync(dir)) {
      for (const file of await readdir(dir)) {
        if (['.md', '.mdx'].includes(extname(file))) slugs.add(basename(file, extname(file)));
      }
    }
    result.set(collection, slugs);
  }
  return result;
}

export function validateItem(item, existing, seen = new Set(), { allowOverwrite = false } = {}) {
  const errors = [];
  const warnings = [];
  if (!COLLECTIONS.has(item.type)) errors.push(`未知 type: ${item.type}`);
  if (!isSafeSlug(item.slug)) errors.push(`slug 不安全: ${item.slug}`);
  if (seen.has(`${item.type}/${item.slug}`)) errors.push(`输入内 slug 冲突: ${item.type}/${item.slug}`);
  seen.add(`${item.type}/${item.slug}`);
  if (!allowOverwrite && existing.get(item.type)?.has(item.slug)) errors.push(`目标已存在: ${item.type}/${item.slug}`);
  for (const key of REQUIRED[item.type] || []) if (!item.data[key]) errors.push(`缺字段 ${key}: ${item.file}`);
  if (!item.body || !item.body.trim()) errors.push(`正文为空: ${item.file}`);
  if (item.data.visibility !== 'public') errors.push(`visibility 不是 public: ${item.file}`);
  if (SECRET_RE.test(item.raw)) errors.push(`疑似 secret/token/key: ${item.file}`);
  if (FORBIDDEN_RE.test(item.raw)) errors.push(`命中禁止发布/私密标记: ${item.file}`);
  if (!Array.isArray(item.data.tags)) warnings.push(`tags 不是数组,同步时会规范化为空数组: ${item.file}`);
  return { errors, warnings };
}

export async function checkInput(args, options = {}) {
  const rawItems = await loadItems(args);
  const existing = await listExistingSlugs(getSiteRoot());
  const seen = new Set();
  const items = [];
  const errors = [];
  const warnings = [];
  for (const rawItem of rawItems) {
    try {
      const item = await readMarkdownItem(rawItem);
      const result = validateItem(item, existing, seen, options);
      errors.push(...result.errors);
      warnings.push(...result.warnings);
      items.push(item);
    } catch (error) {
      errors.push(error.message);
    }
  }
  return { ok: errors.length === 0, errors, warnings, items };
}

export async function writeSyncedItem(item, { overwrite = false } = {}) {
  const siteRoot = getSiteRoot();
  const destDir = join(siteRoot, 'src/content', item.type);
  await mkdir(destDir, { recursive: true });
  const dest = join(destDir, `${item.slug}.md`);
  if (existsSync(dest) && !overwrite) throw new Error(`目标已存在: ${dest}`);
  const data = { ...item.data, tags: Array.isArray(item.data.tags) ? item.data.tags : [], visibility: item.data.visibility || 'public' };
  delete data.slug;
  const body = item.body.trim() + '\n';
  await writeFile(dest, toFrontmatter(data) + body);
  return dest;
}
