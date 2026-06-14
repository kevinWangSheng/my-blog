#!/usr/bin/env node
import { checkInput, parseArgs } from './content-shared.mjs';

const args = parseArgs();
const json = args.json !== false;
try {
  const result = await checkInput(args, { allowOverwrite: Boolean(args.overwrite) });
  const summary = {
    ok: result.ok,
    checked: result.items.length,
    errors: result.errors,
    warnings: result.warnings,
    items: result.items.map((item) => ({ type: item.type, slug: item.slug, file: item.file }))
  };
  console.log(json ? JSON.stringify(summary, null, 2) : `${summary.ok ? 'OK' : 'FAIL'} checked=${summary.checked}`);
  process.exit(summary.ok ? 0 : 1);
} catch (error) {
  console.error(JSON.stringify({ ok: false, errors: [error.message] }, null, 2));
  process.exit(1);
}
