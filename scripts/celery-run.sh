#!/usr/bin/env bash

# -e / errexit | 任何命令返回非 0 时，脚本 立即退出（除非你显式捕获了错误）
# -u / nounset | 使用到未定义的变量时，脚本 立即报错退出（而不是把空字符串当值）
# -o pipefail | 管道中只要任意一个命令失败（退出码非 0），整个管道就 视作失败
# 这是一个业界常见的“安全模式”（strict mode），能让脚本在出现问题时尽早失败，避免隐式地继续往下执行出更难排查的错误
set -euo pipefail

echo "🐘 启动 DB, Redis..."
docker compose up -d db redis

echo "📦 加载环境变量..."
set -a
source .env.local
set +a

echo "🚀 nohub 启动 celery beat, worker ..."
nohup celery -A celery_app beat --loglevel=info 2>&1 &

nohup celery -A celery_app worker --pool=threads --concurrency=1 --loglevel=info 2>&1 &
nohup celery -A celery_app worker --pool=threads --concurrency=1 --loglevel=info 2>&1 &

tail -f nohup.out
