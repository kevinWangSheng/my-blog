#!/usr/bin/env node
/**
 * ui-verify.mjs — 固定 UI 自验证回路(对应 CONVENTIONS.md「UI 自验证回路 ⑥」)。
 *
 * 设计目标(见 DECISIONS.md D-20260614-UI验证工具链 / D-20260614-验证驱动方式):
 *  - 确定性、可重复、低 token:agent 只读 out/summary.json,不必把每张截图回喂。
 *  - 客观信号当「地板」:多断点截图(reduced-motion + 冻结动画)、axe a11y、lighthouse 性能。
 *  - 脱离 agent 也能跑:`pnpm ui-verify -- --serve dist`。
 *  - 截图落盘交给 ⑦ human 看;审美主观判断不在此脚本里做。
 *
 * 用法:
 *   node scripts/ui-verify.mjs --serve <静态目录> [--path /route] [--breakpoints 375,768,1440] [--out out]
 *   node scripts/ui-verify.mjs --url http://localhost:4321 [--path /]
 *   (Astro:先 `astro build` 得到 dist/,再 `--serve dist`;静态产物即可。)
 */
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { extname, join, normalize, resolve, relative } from 'node:path';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

// ---------- args ----------
const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i !== -1 && args[i + 1] ? args[i + 1] : def;
};
const serveDir = getArg('serve', null);
const urlArg = getArg('url', null);
const route = getArg('path', '/');
const outDir = getArg('out', 'out');
const breakpoints = getArg('breakpoints', '375,768,1440')
  .split(',')
  .map((w) => parseInt(w.trim(), 10))
  .filter(Boolean);

if (!serveDir && !urlArg) {
  console.error('ERROR: 需要 --serve <dir> 或 --url <url> 其一');
  process.exit(2);
}
assertSafeOutDir(outDir);


function assertSafeOutDir(dir) {
  const root = resolve('.');
  const target = resolve(dir);
  const rel = relative(root, target);
  if (!rel || rel === '..' || rel.startsWith('..' + '/') || rel.startsWith('..' + '\\')) {
    console.error(`ERROR: --out 必须是仓库内的子目录,收到 ${dir}`);
    process.exit(2);
  }
  if (rel !== 'out' && !rel.startsWith('out/')) {
    console.error(`ERROR: --out 必须是 out 或位于 out/ 下,避免误删源码目录,收到 ${dir}`);
    process.exit(2);
  }
}

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon',
  '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8',
};

// ---------- tiny static server (用于 prototype / Astro dist) ----------
async function startStaticServer(dir) {
  const root = normalize(dir);
  const server = createServer(async (req, res) => {
    try {
      let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      if (p.endsWith('/')) p += 'index.html';
      const filePath = normalize(join(root, p));
      if (!filePath.startsWith(root)) { res.writeHead(403); return res.end('forbidden'); }
      const target = existsSync(join(filePath, 'index.html')) ? join(filePath, 'index.html')
        : existsSync(filePath) ? filePath
        : existsSync(filePath + '.html') ? filePath + '.html'
        : null;
      if (!target) { res.writeHead(404); return res.end('not found'); }
      const body = await readFile(target);
      res.writeHead(200, { 'content-type': MIME[extname(target)] || 'application/octet-stream' });
      res.end(body);
    } catch (e) { res.writeHead(500); res.end(String(e)); }
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const { port } = server.address();
  return { base: `http://127.0.0.1:${port}`, close: () => new Promise((r) => server.close(r)) };
}

// ---------- lighthouse(失败要进入 summary,由主流程判定 ok=false)----------
async function runLighthouse(url) {
  try {
    const { default: lighthouse } = await import('lighthouse');
    const chromeLauncher = await import('chrome-launcher');
    const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless=new', '--no-sandbox'] });
    try {
      const { lhr } = await lighthouse(url, {
        port: chrome.port, output: 'json', logLevel: 'error',
        onlyCategories: ['performance', 'accessibility', 'seo', 'best-practices'],
        formFactor: 'mobile', screenEmulation: { mobile: true, width: 375, height: 812, deviceScaleFactor: 2, disabled: false },
      });
      const scores = Object.fromEntries(
        Object.entries(lhr.categories).map(([k, v]) => [k, v.score == null ? null : Math.round(v.score * 100)])
      );
      const m = lhr.audits;
      return {
        scores,
        metrics: {
          CLS: m['cumulative-layout-shift']?.displayValue ?? null,
          LCP: m['largest-contentful-paint']?.displayValue ?? null,
          TBT: m['total-blocking-time']?.displayValue ?? null,
          FCP: m['first-contentful-paint']?.displayValue ?? null,
        },
      };
    } finally { await chrome.kill(); }
  } catch (e) {
    return { error: String(e?.message || e) };
  }
}

// ---------- main ----------
async function main() {
  await mkdir(outDir, { recursive: true });
  await cleanOwnArtifacts(outDir, breakpoints);

  let staticSrv = null;
  let base = urlArg;
  if (serveDir) {
    if (!existsSync(serveDir)) { console.error(`ERROR: 目录不存在 ${serveDir}`); process.exit(2); }
    staticSrv = await startStaticServer(serveDir);
    base = staticSrv.base;
  }
  const targetUrl = base.replace(/\/$/, '') + route;

  const summary = {
    target: targetUrl, breakpoints, generatedBy: 'ui-verify.mjs',
    screenshots: {}, axe: {}, layout: {}, lighthouse: null, ok: true, problems: [],
  };

  const browser = await chromium.launch();
  try {
    for (const w of breakpoints) {
      const ctx = await browser.newContext({
        viewport: { width: w, height: Math.round(w * 1.6) },
        deviceScaleFactor: 1, reducedMotion: 'reduce',  // emulate prefers-reduced-motion: reduce
      });
      const page = await ctx.newPage();
      const consoleErrors = [];
      const consoleWarnings = [];
      page.on('console', (m) => {
        if (m.type() === 'error') consoleErrors.push(m.text());
        if (m.type() === 'warning') consoleWarnings.push(m.text());
      });

      const resp = await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 30000 });
      const status = resp ? resp.status() : 0;
      if (!resp || status >= 400) { summary.ok = false; summary.problems.push(`HTTP ${status} @ ${w}px`); }

      const overflow = await page.evaluate(() => {
        const doc = document.documentElement;
        const body = document.body;
        const clientWidth = doc.clientWidth;
        const scrollWidth = Math.max(doc.scrollWidth, body?.scrollWidth || 0);
        const tolerance = 1;
        const offenders = Array.from(document.body?.querySelectorAll('*') || [])
          .map((el) => {
            const rect = el.getBoundingClientRect();
            return {
              tag: el.tagName.toLowerCase(),
              className: typeof el.className === 'string' ? el.className : '',
              id: el.id || '',
              left: Math.round(rect.left),
              right: Math.round(rect.right),
              width: Math.round(rect.width),
              text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80),
            };
          })
          .filter((x) => x.width > 0 && (x.right > clientWidth + tolerance || x.left < -tolerance))
          .slice(0, 12);
        return {
          clientWidth,
          scrollWidth,
          overflowX: scrollWidth > clientWidth + tolerance,
          delta: Math.max(0, scrollWidth - clientWidth),
          offenders,
        };
      });
      summary.layout[w] = { horizontalOverflow: overflow };
      if (overflow.overflowX) {
        summary.ok = false;
        summary.problems.push(`horizontal overflow @ ${w}px: scrollWidth=${overflow.scrollWidth}, clientWidth=${overflow.clientWidth}, delta=${overflow.delta}`);
      }

      const shot = join(outDir, `screen-${w}.png`);
      await page.screenshot({ path: shot, fullPage: true, animations: 'disabled' });
      summary.screenshots[w] = { file: shot, status, consoleErrors, consoleWarnings };
      if (consoleErrors.length) { summary.ok = false; summary.problems.push(`${consoleErrors.length} console error(s) @ ${w}px`); }
      if (consoleWarnings.length) { summary.ok = false; summary.problems.push(`${consoleWarnings.length} console warning(s) @ ${w}px`); }

      // axe a11y
      try {
        const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
        const bySeverity = (sev) => results.violations.filter((v) => v.impact === sev).length;
        const v = results.violations;
        await writeFile(join(outDir, `axe-${w}.json`), JSON.stringify(v, null, 2));
        summary.axe[w] = {
          total: v.length,
          critical: bySeverity('critical'), serious: bySeverity('serious'),
          moderate: bySeverity('moderate'), minor: bySeverity('minor'),
          rules: v.slice(0, 8).map((x) => ({ id: x.id, impact: x.impact, nodes: x.nodes.length, help: x.help })),
        };
        if (bySeverity('critical') || bySeverity('serious')) {
          summary.ok = false;
          summary.problems.push(`axe critical/serious @ ${w}px: ${bySeverity('critical')}/${bySeverity('serious')}`);
        }
      } catch (e) {
        summary.ok = false;
        summary.axe[w] = { error: String(e?.message || e) };
        summary.problems.push(`axe error @ ${w}px: ${String(e?.message || e)}`);
      }
      await ctx.close();
    }
  } finally {
    await browser.close();
  }

  summary.lighthouse = await runLighthouse(targetUrl);
  if (summary.lighthouse?.scores) {
    for (const [cat, val] of Object.entries(summary.lighthouse.scores)) {
      if (val != null && val < 80) {
        summary.ok = false;
        summary.problems.push(`lighthouse ${cat}=${val} (<80)`);
      }
    }
  } else if (summary.lighthouse?.error) {
    summary.ok = false;
    summary.problems.push(`lighthouse error: ${summary.lighthouse.error}`);
  }

  if (staticSrv) await staticSrv.close();
  await writeFile(join(outDir, 'summary.json'), JSON.stringify(summary, null, 2));

  // 控制台精简汇总(给 agent / 人快速看)
  console.log('\n=== ui-verify summary ===');
  console.log('target:', summary.target);
  for (const w of breakpoints) {
    const a = summary.axe[w] || {};
    const overflow = summary.layout[w]?.horizontalOverflow;
    console.log(`  [${w}px] shot=${summary.screenshots[w]?.file} axe=${a.error ? 'ERR' : `${a.total} (crit ${a.critical}/serious ${a.serious})`} consoleErr=${summary.screenshots[w]?.consoleErrors?.length ?? '?'} consoleWarn=${summary.screenshots[w]?.consoleWarnings?.length ?? '?'} overflow=${overflow?.overflowX ? `YES(+${overflow.delta}px)` : 'no'}`);
  }
  console.log('  lighthouse:', summary.lighthouse?.scores ? JSON.stringify(summary.lighthouse.scores) : `ERROR (${summary.lighthouse?.error})`);
  console.log('  problems:', summary.problems.length ? summary.problems.join('; ') : '(none)');
  console.log('  OK:', summary.ok);
  console.log('  详见', join(outDir, 'summary.json'));
  process.exit(summary.ok ? 0 : 1);
}

async function cleanOwnArtifacts(dir, widths) {
  await Promise.all([
    rm(join(dir, 'summary.json'), { force: true }),
    ...widths.map((w) => rm(join(dir, `screen-${w}.png`), { force: true })),
  ]);
}

main().catch((e) => { console.error(e); process.exit(1); });
