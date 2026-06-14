#!/usr/bin/env node
import { checkInput, parseArgs, writeSyncedItem } from './content-shared.mjs';

const args = parseArgs();
const overwrite = Boolean(args.overwrite);
try {
  const result = await checkInput(args, { allowOverwrite: overwrite });
  if (!result.ok) {
    console.error(JSON.stringify({ ok: false, phase: 'check', errors: result.errors, warnings: result.warnings }, null, 2));
    process.exit(1);
  }
  const written = [];
  for (const item of result.items) {
    const dest = await writeSyncedItem(item, { overwrite });
    written.push({ type: item.type, slug: item.slug, path: dest });
  }
  console.log(JSON.stringify({ ok: true, written, skipped: [], warnings: result.warnings }, null, 2));
} catch (error) {
  console.error(JSON.stringify({ ok: false, phase: 'sync', errors: [error.message] }, null, 2));
  process.exit(1);
}
