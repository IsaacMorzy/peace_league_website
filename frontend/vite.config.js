/** @type {import('astro').AstroConfig} */
export default {
  vite: {
    plugins: [tailwindcss()],
    build: {
      rollupOptions: {
        input: {
          'main': './src/entry-client.ts',
        },
      },
    },
  },
};
