# sentry-docker尝试

```yml
# Sentry 服务
sentry:
  image: sentry:latest
  container_name: news-summary-sentry
  depends_on:
    - sentry-postgres
    - sentry-redis
  environment:
    SENTRY_SECRET_KEY: "your-sentry-secret-key"
    SENTRY_POSTGRES_HOST: sentry-postgres
    SENTRY_DB_USER: sentry
    SENTRY_DB_PASSWORD: sentry
    SENTRY_DB_NAME: sentry
    SENTRY_REDIS_HOST: sentry-redis
  ports:
    - "9000:9000"
  networks:
    - app-network
  command: |
    bash -c "
    sentry upgrade --noinput &&
    sentry run web"

  # Sentry 的 PostgreSQL 数据库
sentry-postgres:
  image: postgres:16
  container_name: news-summary-sentry-postgres
  environment:
    POSTGRES_USER: sentry
    POSTGRES_PASSWORD: sentry
    POSTGRES_DB: sentry
  volumes:
    - sentry_postgres_data:/var/lib/postgresql/data
  networks:
    - app-network

    #Sentry 的 Redis
sentry-redis:
  image: redis:6
  container_name: news-summary-sentry-redis
  volumes:
    - sentry_redis_data:/data
  networks:
    - app-network

volumes:
  sentry_postgres_data:
  sentry_redis_data:
```
