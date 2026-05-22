import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

import { collectRoutesFromPages } from './collect-routes.mjs';

test('collectRoutesFromPages builds expected routes', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pla-pages-'));
  const pages = path.join(tmp, 'pages');
  fs.mkdirSync(pages, { recursive: true });

  fs.writeFileSync(path.join(pages, 'index.astro'), '');
  fs.writeFileSync(path.join(pages, 'about.astro'), '');

  fs.mkdirSync(path.join(pages, 'blog'), { recursive: true });
  fs.writeFileSync(path.join(pages, 'blog', 'index.astro'), '');
  fs.writeFileSync(path.join(pages, 'blog', '[slug].astro'), '');

  fs.mkdirSync(path.join(pages, 'api'), { recursive: true });
  fs.writeFileSync(path.join(pages, 'api', 'ping.astro'), '');

  const routes = collectRoutesFromPages(pages);
  assert.deepEqual(routes, ['/', '/about', '/blog']);
});