#!/bin/sh
set -e

echo "⏰ 启动 Celery Beat."
exec celery -A celery_app beat --loglevel=info
