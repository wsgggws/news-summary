#!/usr/bin/env bash

set -euo pipefail

echo "📦 关闭旧容器..."
docker compose down db test-db -v || true
echo "🐘 启动 PostgreSQL test-db 数据库..."
docker compose up -d test-db

echo "🔧 加载 CI 环境变量 (.env.ci)..."
set -a
source .env.ci
set +a

# 如果没有传参，则直接跑 pytest
if [ $# -eq 0 ]; then
  echo "🧪 运行所有测试 (默认)..."
  pytest
else
  echo "🧪 运行 pytest with args: $*"
  pytest "$@"
fi
