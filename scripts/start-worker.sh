#!/bin/sh
set -e

# $1 是 worker 名称，例如 worker1、worker2
if [ -z "$1" ]; then
  echo "❌ 请提供 worker 名称作为参数"
  exit 1
fi

echo "🚀 启动 Celery Worker：$1"
exec python3.11 -m celery -A celery_app worker \
  --hostname="$1" \
  --pool=threads \
  --concurrency=1 \
  --loglevel=info
