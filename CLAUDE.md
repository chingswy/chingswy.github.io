# CLAUDE.md — 项目开发规范

## 1. 项目概述

基于 Jekyll + al-folio 主题的学术个人网站，使用 Ruby 构建，部署在 GitHub Pages。

## 2. 本地开发

```bash
# 安装依赖（首次）
brew install rbenv ruby-build imagemagick
rbenv install 3.2.3 && rbenv local 3.2.3
eval "$(rbenv init - zsh)"
gem install bundler && bundle install

# 启动本地服务
./restart.sh
# 或手动: bundle exec jekyll serve --port 8080 --livereload
```

## 3. 设计风格：Apple 毛玻璃

整体视觉对标 macOS 系统设置 / Apple 官网的克制美学。

### 核心要素

- **背景**：`#f5f5f7` 纯暖灰，不使用多色渐变
- **卡片**：半透明白色（`rgba(255,255,255,0.72)`）+ `backdrop-filter: blur(20px)` + `border: border-white/50` + 柔和阴影
- **导航栏**：sticky 毛玻璃（`saturate(180%) blur(20px)`），活跃项用 `bg-white/60` 胶囊
- **圆角**：统一 12–16px（`rounded-xl` / `rounded-2xl`）
- **阴影**：多级别柔和阴影（`shadow-glass` / `shadow-glass-lg` / `shadow-glass-sm`）

### 颜色规范

- **主色**：`#1d1d1f`（Apple 近黑色），用于主按钮、Toggle 开启态、分页当前页
- **文字**：`gray-800`（正文）、`gray-500`（标签/标题）、`gray-400`（辅助信息）
- **状态色**：`emerald-400/600`（成功）、`red-400/500`（失败）、`blue-400/500`（处理中）、`amber-500`（警告）
- **表单聚焦**：`ring-gray-300/60`

### 禁止事项

- **禁止使用渐变色**（linear-gradient）作为按钮、文字、Toggle 等 UI 元素的填充色。渐变色看起来像 AI 生成，不够高级
- **禁止使用 indigo / purple 系列色**。强调色统一用近黑色或状态语义色
- 不要在非数据可视化场景使用彩色填充

---

## 4. 样式约定

### CSS 组件类（定义在 `_sass/_base.scss`）

| 类名 | 用途 |
|---|---|
| `.glass-card` | 毛玻璃卡片基础样式 |
| `.glass-card-hover` | 带 hover 上浮效果的毛玻璃卡片 |
| `.repo-card-box` | GitHub 仓库卡片 |

### 内嵌统计块

数值统计使用内嵌的 `p-3 rounded-xl bg-white/40 text-center` 作为子卡片，不要用纯文字裸排。

### 表格

- 圆角 `rounded-xl overflow-hidden` 包裹
- 行分隔用半透明边框，融入毛玻璃
- hover 用 `hover:bg-white/40` 或 `hover:bg-white/50`

---

## 5. 文件结构

| 路径 | 说明 |
|---|---|
| `_pages/about.md` | 首页内容 |
| `_bibliography/papers.bib` | 论文列表（BibTeX） |
| `_data/repositories.yml` | GitHub 仓库配置 |
| `_config.yml` | 全站配置 |
| `_sass/_themes.scss` | 主题色变量（light/dark） |
| `_sass/_variables.scss` | SCSS 变量 |
| `_sass/_base.scss` | 基础样式 |
| `_includes/header.html` | 导航栏 |
| `_includes/repository/repo.html` | GitHub 卡片模板 |
| `_layouts/about.html` | 首页 layout |
