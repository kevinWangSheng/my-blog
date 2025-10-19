# Hugo博客搭建完整计划

## 项目概述

**目标**: 搭建一个基于Hugo + Notion的个人技术博客,支持自动同步和部署

**技术栈**:

- 静态生成器: Hugo
- 主题: Stack (暗色极客风格)
- CMS: Notion
- 部署: Vercel
- 自动化: GitHub Actions

**仓库地址**: git@github.com:kevinWangSheng/my-blog.git

---

## 阶段一: 初始化Hugo博客项目

### 任务1.1: 清理并重建Git仓库

```bash
# 当前位置: /root/my-blog
# 删除现有的git配置
rm -rf .git

# 重新初始化
git init
git branch -M main
```

### 任务1.2: 配置.gitignore

创建 `.gitignore` 文件:

```gitignore
public/
resources/_gen/
.hugo_build.lock
.DS_Store
node_modules/
```

### 任务1.3: 更新config.yaml配置

修改 `config.yaml`:

```yaml
baseURL: https://kevinwangsheng.vercel.app/
languageCode: zh-cn
title: Kevin的技术日志
theme: stack
hasCJKLanguage: true

params:
  mainSections:
    - posts
  
  sidebar:
    emoji: 💻
    subtitle: Java后端开发 | Rust学习者 | 每日技术记录
    avatar:
      enabled: false
  
  article:
    math: false
    toc: true
    readingTime: true
    license:
      enabled: false
  
  comments:
    enabled: false
  
  colorScheme:
    toggle: true
    default: dark

menu:
  main:
    - identifier: home
      name: 首页
      url: /
      weight: 1
    - identifier: archives
      name: 归档
      url: /archives/
      weight: 2
    - identifier: categories
      name: 分类
      url: /categories/
      weight: 3
    - identifier: tags
      name: 标签
      url: /tags/
      weight: 4

markup:
  highlight:
    style: monokai
    lineNos: true
  goldmark:
    renderer:
      unsafe: true
```

---

## 阶段二: 创建示例内容

### 任务2.1: 创建第一篇文章

创建 `content/posts/first-post.md`:

```markdown
---
title: "开始我的技术博客之旅"
date: 2025-01-19T20:00:00+08:00
draft: false
description: "搭建Hugo + Notion博客系统"
tags: ["博客", "Hugo"]
categories: ["技术"]
---

## 今天完成的事情

成功搭建了自己的技术博客!

### 使用的技术
- Hugo静态网站生成器
- Stack主题(暗色风格)
- Notion作为内容管理系统
- GitHub Actions自动化部署

### 下一步计划
- 配置Notion自动同步
- 部署到Vercel
- 开始记录每日学习

Let's go! 🚀
```

### 任务2.2: 创建Rust学习笔记

创建 `content/posts/rust-learning.md`:

```markdown
---
title: "Rust学习笔记 - 所有权系统"
date: 2025-01-19T21:00:00+08:00
draft: false
tags: ["Rust", "学习笔记"]
categories: ["技术"]
---

## 所有权系统核心概念

### 三大规则
1. 每个值都有一个所有者
2. 同一时间只能有一个所有者
3. 所有者离开作用域,值被丢弃

### 代码示例

\`\`\`rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1的所有权转移给s2
    // println!("{}", s1); // 错误!s1已失效
    println!("{}", s2); // OK
}
\`\`\`

### 今日收获
理解了Rust如何在编译期保证内存安全!
```

### 任务2.3: 创建Java后端笔记

创建 `content/posts/java-backend.md`:

```markdown
---
title: "Java后端开发笔记 - Spring Boot最佳实践"
date: 2025-01-19T22:00:00+08:00
draft: false
tags: ["Java", "Spring Boot"]
categories: ["技术"]
---

## Spring Boot项目结构

### 推荐的分层架构

\`\`\`
├── controller   # 控制器层
├── service      # 业务逻辑层
├── repository   # 数据访问层
├── entity       # 实体类
├── dto          # 数据传输对象
└── config       # 配置类
\`\`\`

### 常用注解

- `@RestController`: REST API控制器
- `@Service`: 服务层组件
- `@Repository`: 数据访问层
- `@Autowired`: 自动注入

### 最佳实践
1. 使用DTO而不是直接返回Entity
2. 统一异常处理
3. 参数校验使用@Valid
4. 日志记录使用SLF4J

持续学习,持续进步! 💪
```

### 任务2.4: 创建关于页面

创建 `content/about.md`:

```markdown
---
title: "关于我"
date: 2025-01-19
layout: "page"
slug: "about"
menu:
    main:
        weight: 5
        params: 
            icon: user
---

## 👋 你好

我是Kevin,一名Java后端开发工程师,正在学习Rust。

### 💼 技术栈
- **后端**: Java, Spring Boot, MySQL, Redis
- **学习中**: Rust, Tokio, 异步编程
- **工具**: Git, Docker, Linux

### 📝 博客目标
记录每日学习和工作,分享技术笔记,追踪个人成长。

### 🎯 2025年目标
- 深入掌握Rust编程
- 学习系统编程和性能优化
- 每周至少更新2篇技术文章
- 完成1个Rust开源项目

### 📫 联系方式
- GitHub: [@kevinWangSheng](https://github.com/kevinWangSheng)
```

---

## 阶段三: 配置Notion自动同步

### 任务3.1: 创建GitHub Actions配置

创建 `.github/workflows/notion-sync.yml`:

```yaml
name: Notion同步到Hugo

on:
  schedule:
    - cron: '0 */6 * * *'  # 每6小时自动同步
  workflow_dispatch:  # 允许手动触发

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install notion-to-md
        run: npm install -g notion-to-md

      - name: Sync from Notion
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
          DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
        run: |
          notion2md -n $NOTION_TOKEN -d $DATABASE_ID -o content/posts

      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff-index --quiet HEAD || git commit -m "Sync from Notion [$(date +'%Y-%m-%d %H:%M:%S')]"

      - name: Push changes
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          branch: main
```

---

## 阶段四: 推送到GitHub

### 任务4.1: 提交所有文件

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Initial blog setup with Hugo + Stack theme"
```

### 任务4.2: 连接GitHub并推送

```bash
# 添加远程仓库(SSH方式)
git remote add origin git@github.com:kevinWangSheng/my-blog.git

# 拉取远程并合并(如果有README等文件)
git pull origin main --allow-unrelated-histories --no-edit

# 推送到GitHub
git push -u origin main
```

---

## 阶段五: 配置Vercel部署

### 任务5.1: 创建vercel.json配置

创建 `vercel.json`:

```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.122.0"
    }
  }
}
```

---

## 手动操作清单

### 1. 配置GitHub Secrets

在GitHub仓库 `https://github.com/kevinWangSheng/my-blog` 中:

1. 进入 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加两个secrets:

```
Name: NOTION_TOKEN
Value: <你的Notion Integration Token>

Name: NOTION_DATABASE_ID
Value: <你的Notion数据库ID>
```

### 2. 部署到Vercel

1. 访问 https://vercel.com
2. 用GitHub账号登录
3. 点击 "Add New..." → "Project"
4. 选择 `kevinWangSheng/my-blog` 仓库
5. 配置:
   - Framework Preset: Hugo
   - Build Command: `hugo --gc --minify`
   - Output Directory: `public`
   - Environment Variables: `HUGO_VERSION` = `0.122.0`
6. 点击 "Deploy"

---

## 验证清单

完成后检查:

- [ ] 本地 `hugo server -D` 能正常运行
- [ ] GitHub仓库有所有文件
- [ ] GitHub Actions配置正确(.github/workflows/notion-sync.yml存在)
- [ ] GitHub Secrets已添加
- [ ] Vercel成功部署
- [ ] 访问 `xxx.vercel.app` 能看到博客
- [ ] 博客有4篇文章(首页、Rust、Java、关于)
- [ ] 暗色主题正常工作
- [ ] 代码高亮显示正常

---

## 给Claude Code的执行指令

```
请帮我完成Hugo博客的搭建,当前目录是 /root/my-blog:

1. 清理.git并重新初始化Git仓库
2. 创建.gitignore文件
3. 更新config.yaml配置为中文极客风格
4. 创建4篇示例文章:
   - content/posts/first-post.md (开始博客)
   - content/posts/rust-learning.md (Rust学习)
   - content/posts/java-backend.md (Java后端)
   - content/about.md (关于页面)
5. 创建.github/workflows/notion-sync.yml用于Notion自动同步
6. 创建vercel.json配置文件
7. 提交所有更改并推送到 git@github.com:kevinWangSheng/my-blog.git

注意事项:
- 使用SSH方式连接GitHub
- 如果远程有内容,先 git pull origin main --allow-unrelated-histories --no-edit
- 然后再 git push -u origin main
- 主题(themes/stack)已经存在,不需要重新下载
- 确保所有Markdown文件使用UTF-8编码
```

---

## 工作流程图

```
Notion写文章
    ↓
设置状态为"已发布"
    ↓
GitHub Actions自动同步 (每6小时或手动触发)
    ↓
推送到GitHub仓库
    ↓
Vercel检测到更新
    ↓
自动构建并部署
    ↓
博客自动更新! ✨
```

---

## 常见问题

### Q1: 本地预览没问题,部署后样式丢失?

A: 检查config.yaml中的baseURL是否正确设置为Vercel域名

### Q2: Notion同步不工作?

A: 检查GitHub Secrets是否正确添加,Notion数据库是否正确分享给Integration

### Q3: 推送时提示认证失败?

A: 确认使用SSH地址(git@github.com:...)而不是HTTPS地址

### Q4: 本地运行报错找不到主题?

A: 运行 `git submodule update --init --recursive`

---

## 后续优化建议

1. **添加评论系统**: giscus或utterances
2. **添加网站统计**: Google Analytics或umami
3. **自定义域名**: 在Vercel绑定自己的域名
4. **优化SEO**: 添加sitemap和robots.txt
5. **添加RSS订阅**: Hugo自动生成RSS feed
6. **图片优化**: 使用图床或压缩图片

---

## 参考资料

- Hugo官方文档: https://gohugo.io/documentation/
- Stack主题文档: https://stack.jimmycai.com/
- Notion API文档: https://developers.notion.com/
- Vercel部署文档: https://vercel.com/docs

---

**文档版本**: v1.0  
**创建日期**: 2025-01-19  
**作者**: Kevin Wang  
**最后更新**: 2025-01-19
