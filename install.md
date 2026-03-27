# 本地环境安装指南 (macOS)

## 前置要求

- macOS 系统
- [Homebrew](https://brew.sh/) 已安装

## 1. 安装 rbenv 和 Ruby

```bash
# 安装 rbenv 和 ruby-build
brew install rbenv ruby-build

# 安装 Ruby 3.2.3
rbenv install 3.2.3

# 在项目目录下设置 Ruby 版本
rbenv local 3.2.3

# 初始化 rbenv（建议将此行加入 ~/.zshrc）
eval "$(rbenv init - zsh)"

# 验证 Ruby 版本
ruby --version
```

## 2. 安装 ImageMagick

```bash
brew install imagemagick
```

jekyll-imagemagick 插件依赖此工具，用于自动生成响应式 WebP 图片。

## 3. 安装 Gem 依赖

```bash
# 安装 Bundler
gem install bundler

# 安装项目所有依赖
bundle install
```

> **注意**：`mini_racer` / `libv8-node` 包含 V8 引擎原生代码，编译较慢，请耐心等待。

## 4. 启动本地服务

```bash
bundle exec jekyll serve --port 8080 --livereload
```

浏览器访问 http://localhost:8080/ 即可预览网站。

## 常见问题

### rbenv 每次打开终端都要手动初始化？

将以下内容加入 `~/.zshrc`：

```bash
eval "$(rbenv init - zsh)"
```

### bundle install 报错？

确保使用的是 rbenv 管理的 Ruby，而非系统自带的旧版本：

```bash
which ruby   # 应输出 ~/.rbenv/shims/ruby
ruby --version  # 应为 3.2.3
```
