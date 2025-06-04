#!/usr/bin/env bash
set -euo pipefail

echo "📦 关闭旧容器..."
docker compose down || true # 防止第一次部署时报错

echo "📦 加载环境变量..."
set -a
source .env.docker
set +a

echo "🚀 启动 FastAPI 开发服务..."
docker compose up --build web nginx celery-worker1 celery-worker2 celery-beat -d
