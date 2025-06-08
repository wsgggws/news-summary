#!/usr/bin/env bash
set -euo pipefail

echo "📦 关闭旧容器 web celery-worker celery-beat."
docker compose down web celery-worker celery-beat || true

echo "📦 加载环境变量 .env.docker .env"
set -a
source .env.docker
source .env
set +a

echo "🚀 启动容器 web celery-worker celery-beat."
docker compose up --build web celery-worker celery-beat -d

# nginx: 启动或重启
NGINX_ID=$(docker compose ps -q nginx)

if [[ -z "$NGINX_ID" ]] || [[ "$(docker inspect -f '{{.State.Running}}' "$NGINX_ID" 2>/dev/null)" != "true" ]]; then
  echo "🚀 nginx 未启动，开始启动 nginx"
  docker compose up -d nginx
else
  echo "🔁 nginx 已在运行，执行重启"
  docker compose restart nginx
fi
