#!/usr/bin/env bash

set -euo pipefail

mkdir -p .log .pids

echo "🐘 启动 DB, Redis..."
docker compose up -d db redis

echo "📦 加载环境变量..."
set -a
source .env.local
set +a

echo "🚀 启动 Celery beat 和 worker ..."

# 启动 Celery Beat
celery -A celery_app beat --loglevel=info >.log/celery_beat.log 2>&1 &
echo $! >.pids/celery_beat.pid
echo "✅ celery_beat 启动，PID: $(cat .pids/celery_beat.pid)"

# 启动两个 Celery Worker
for i in 1 2; do
  celery -A celery_app worker --pool=threads --concurrency=1 --loglevel=info >".log/celery_worker_${i}.log" 2>&1 &
  echo $! >".pids/celery_worker_${i}.pid"
  echo "✅ celery_worker_${i} 启动，PID: $(cat .pids/celery_worker_${i}.pid)"
done

echo "📡 正在输出日志中（按 Ctrl+C 停止 tail，不会终止 celery）"
tail -f .log/celery_*.log
