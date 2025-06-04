#!/bin/sh
set -e

echo "⏰ 启动 Celery Beat..."
exec python3.11 -m celery -A celery_app beat --loglevel=info
