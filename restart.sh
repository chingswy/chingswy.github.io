#!/bin/bash
# 启动 Jekyll 本地开发服务器
# 用法: ./restart.sh

# 初始化 rbenv
eval "$(rbenv init - zsh)"

# 停止已有的 Jekyll 进程（如果有）
pkill -f "jekyll serve" 2>/dev/null

# 删除旧的 Gemfile.lock 避免依赖冲突
rm -f Gemfile.lock

# 启动 Jekyll 服务
bundle exec jekyll serve --port 8080 --livereload

# 浏览器访问: http://localhost:8080/
