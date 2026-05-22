import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function isDynamicRoute(filePath) {
  return filePath.includes('[') && filePath.includes(']');
}

function isApiRoute(filePath) {
  return filePath.split(path.sep).includes('api');
}

export function collectRoutesFromPages(pagesRoot) {
  const astroFiles = walk(pagesRoot).filter((file) => file.endsWith('.astro'));
  const routes = [];

  for (const filePath of astroFiles) {
    const rel = path.relative(pagesRoot, filePath);
    const parsed = path.parse(rel);

    if (isDynamicRoute(rel) || isApiRoute(rel)) {
      continue;
    }

    if (parsed.name === '404') {
      continue;
    }

    const segments = rel
      .replace(/\.astro$/, '')
      .split(path.sep)
      .filter(Boolean);

    if (segments.length > 0 && segments[segments.length - 1] === 'index') {
      segments.pop();
    }

    const route = `/${segments.join('/')}`.replace(/\/$/, '') || '/';
    routes.push(route === '' ? '/' : route);
  }

  return Array.from(new Set(routes)).sort();
}

function getArgValue(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return null;
  return process.argv[idx + 1] || null;
}

if (process.argv[1] === __filename) {
  const pagesRoot = getArgValue('--pages') || path.resolve(__dirname, '../src/pages');
  const outFile = getArgValue('--out');
  const routes = collectRoutesFromPages(path.resolve(pagesRoot));
  const output = `${routes.join('\n')}\n`;

  if (outFile) {
    fs.mkdirSync(path.dirname(outFile), { recursive: true });
    fs.writeFileSync(outFile, output);
  } else {
    process.stdout.write(output);
  }
}
