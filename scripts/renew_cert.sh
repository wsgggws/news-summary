#!/bin/bash

echo "============================================"
echo "Certbot renewal attempt started at $(date)"
echo "============================================"

# 尝试续期所有证书
certbot renew \
  --config-dir="$(pwd)/data/certbot/conf" \
  --work-dir="$(pwd)/data/certbot/conf" \
  --logs-dir="$(pwd)/data/certbot/conf/logs" \
  --quiet

# 重启 Nginx 应用新证书
docker compose restart nginx

echo "Certbot renewal completed at $(date)"
echo "============================================"
