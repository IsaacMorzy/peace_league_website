import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.resolve(__dirname, '..', 'dist');
const port = parseInt(process.argv[2] || '4321', 10);
const host = process.argv[3] || '0.0.0.0';

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.mjs': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.txt': 'text/plain',
  '.xml': 'application/xml',
  '.map': 'application/json',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(distDir, req.url === '/' ? 'index.html' : req.url);
  if (!filePath.startsWith(distDir)) { res.writeHead(403); res.end(); return; }
  
  if (!fs.existsSync(filePath)) {
    const htmlPath = path.join(filePath, 'index.html');
    if (fs.existsSync(htmlPath)) filePath = htmlPath;
    else if (fs.existsSync(filePath + '.html')) filePath = filePath + '.html';
  }
  
  if (!fs.existsSync(filePath)) {
    const fallback = path.join(distDir, '404.html');
    if (fs.existsSync(fallback)) filePath = fallback;
  }

  if (!fs.existsSync(filePath)) {
    res.writeHead(404); res.end('Not found');
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME[ext] || 'application/octet-stream';

  const raw = fs.readFileSync(filePath);
  if (ext === '.html') {
    res.setHeader('Content-Type', contentType + '; charset=utf-8');
  } else {
    res.setHeader('Content-Type', contentType);
  }
  res.writeHead(200);
  res.end(raw);
});

server.listen(port, host, () => {
  console.log(`Static server at http://${host}:${port}/`);
});
