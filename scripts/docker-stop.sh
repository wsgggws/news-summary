#!/usr/bin/env bash
set -euo pipefail

echo "📦 停止并移除指定容器：web celery-worker celery-beat"
docker compose rm -fsv web celery-worker celery-beat || true

echo "✅ 已停止并清理指定容器。"
