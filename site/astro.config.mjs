import { defineConfig } from 'astro/config';

// 方向 B 代码块主题 —— 颜色镜像 tokens.css 的 --c-code-* (shiki 在构建期运行,无法读 CSS 变量,故此处硬编码同值)。
const warmGardenCode = {
  name: 'warm-garden-dark',
  type: 'dark',
  colors: { 'editor.background': '#1f2b26', 'editor.foreground': '#d7e3dc' },
  settings: [
    { settings: { background: '#1f2b26', foreground: '#d7e3dc' } },
    { scope: ['comment', 'punctuation.definition.comment'], settings: { foreground: '#7f9488', fontStyle: 'italic' } },
    { scope: ['keyword', 'storage', 'storage.type', 'keyword.control', 'keyword.operator', 'variable.language'], settings: { foreground: '#e6b877' } },
    { scope: ['string', 'string.quoted', 'punctuation.definition.string', 'constant.character'], settings: { foreground: '#7ed3a8' } },
    { scope: ['entity.name.function', 'support.function', 'meta.function-call', 'entity.name.tag'], settings: { foreground: '#8fc4d6' } },
    { scope: ['constant.numeric', 'constant.language', 'support.constant', 'entity.name.type', 'support.type'], settings: { foreground: '#8fc4d6' } },
    { scope: ['variable', 'variable.parameter', 'meta.definition.variable'], settings: { foreground: '#d7e3dc' } }
  ]
};

export default defineConfig({
  site: 'https://kevinwangsheng.github.io',
  base: '/my-blog',
  output: 'static',
  trailingSlash: 'never',
  markdown: {
    shikiConfig: { theme: warmGardenCode, wrap: false }
  }
});
