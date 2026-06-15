import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://kevinwangsheng.github.io',
  base: '/my-blog',
  output: 'static',
  trailingSlash: 'never'
});
