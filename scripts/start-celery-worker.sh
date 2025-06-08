#!/bin/sh
set -e

echo "🚀 启动 Celery Worker."
exec celery -A celery_app worker --concurrency=2 --loglevel=info
