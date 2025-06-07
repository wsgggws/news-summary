#!/usr/bin/env bash
set -euo pipefail

echo "📦 关闭旧容器 web celery-worker celery-beat."
docker compose down web celery-worker celery-beat -v || true # 防止第一次部署时报错

echo "📦 加载环境变量 .env.docker .env"
set -a
source .env.docker
source .env
set +a

echo "🚀 启动容器 web celery-worker celery-beat."
docker compose up --build web celery-worker celery-beat -d
