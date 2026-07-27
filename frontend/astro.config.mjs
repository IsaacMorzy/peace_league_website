// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://peaceleagueafrica.org',
  outDir: '../peace_league_website/public/astro_pages',  // canonical Frappe-bench public path for deploy.sh
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()]
  }
});
