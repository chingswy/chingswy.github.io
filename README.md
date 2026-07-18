# chingswy.github.io

个人主页 · Astro + Tailwind CSS 4 + GitHub Pages

## 本地开发

```bash
npm install       # 首次
npm run dev       # 启动开发服务器，默认 http://localhost:4321
npm run build     # 生产构建，输出到 dist/
npm run preview   # 预览构建产物
```

Node 20+。首次 `npm install` 走了本地 `.npmrc` 里的淘宝镜像；CI 用官方源。

## 部署

Push 到 `main` 分支后，`.github/workflows/deploy.yml` 自动构建并发布到 GitHub Pages。

**首次启用（一次性）：**
1. GitHub 仓库 → Settings → Pages → Source 选 **GitHub Actions**
2. Push 一次 main

## 目录结构

```
src/
├── components/
│   └── Viewer3D.astro   3D 头像（three.js + GLTFLoader）
├── layouts/
│   └── Base.astro       整站骨架 + 翻页控制脚本
├── pages/
│   └── index.astro      单页站点，所有 section 都在这里
└── styles/
    └── global.css       design tokens + deck 翻页动画
public/
├── qing-202206.glb      3D 模型
└── favicon.svg
```

## 设计逻辑

**结构**：单页站点，四个 section 依次是 Home（3D 头像 + Bio）→ Experience → Projects → Publications。

**翻页交互**（Base.astro 中的脚本）：所有 section 绝对定位叠放，翻页时旧页淡出 + 微上移 8px、新页从下方 12px 淡入 —— 参考 Keynote Dissolve。**关键点**：不做 100vh 整块位移，眼睛感知的是"内容替换"而不是"电梯位移"，不晕。默认 620ms、`cubic-bezier(0.32, 0.72, 0, 1)`。到达页面时其内元素做 stagger 上移淡入（120/200/260/300ms），给眼睛提供焦点。

**输入处理**：
- 拦截 wheel，累积 deltaY 到 40 才翻一页，翻完锁 620ms —— 触摸板惯性不会连翻多页
- 动画期间**吞掉所有 wheel 事件**，避免余波把 Publications 页原生滚到底
- Publications 页标 `.scrollable`：内容超出时内部可滚，只在滚到顶/底后 wheel 才驱动翻页
- 键盘 ↑↓/PgUp/PgDn/Space/Home/End；触屏上下滑；URL hash 同步；右侧圆点导航可点击直达

**视觉语言**（对齐苹果的克制感）：
- 字体：**Newsreader**（正文衬线）+ **Inter**（meta/UI 无衬线）
- 主色：靖蓝 `#3d5a80`（暗色柔化 `#98b6dc`），灰阶用 iOS 系统色 `#1c1c1e` / `#48484a` / `#8e8e93`
- 链接用 `border-bottom` 而非 `text-decoration`（更细、更好控距）
- 无卡片边框、无 hover 位移、无 §01 类学术编号、几乎不用斜体做强调
- 3D 头像的"Drag to view"仅悬停时淡出，不喧宾夺主

**颜色/字体调整**：编辑 `src/styles/global.css` 顶部的 `@theme` 与 `:root` / `:root.dark` 变量即可。

**主题切换**：右上角 FAB，`localStorage` 记忆，脚本在首屏 paint 前应用主题避免闪烁。

## 内容位置

目前 Experience / Projects / Publications 的数据硬编码在 `src/pages/index.astro` 顶部的 frontmatter 里。等版式定稿后，可迁移到 Astro content collections（`src/content/`），用 Markdown/YAML 维护。
