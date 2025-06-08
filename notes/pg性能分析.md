# PG 性能分析

## 生成 postgresql sample 文件

```sh
docker run --rm postgres:16 cat /usr/share/postgresql/postgresql.conf.sample > ./config/postgres/postgresql.conf
```

## 添加配置

```conf
max_connections = 200
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql.log'
log_min_duration_statement = 500
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d '

# 启用扩展所需共享内存（例如 pg_stat_statements）
shared_preload_libraries = 'pg_stat_statements'

# 可选，开启查询缓存命中分析
track_io_timing = on
```

## 修改 docker-compose.yaml

```yml
volumes:
  - ./data/postgres:/var/lib/postgresql/data
  - ./config/postgres/postgresql.conf:/etc/postgresql/postgresql.conf
ports:
  - "127.0.0.1:5432:5432" # 本地 web 连接, SSH 隧道访问 PostgreSQL
command: postgres -c config_file=/etc/postgresql/postgresql.conf
```

## 启用扩展

```sh
# 所以可以用这个 user 用户登录（假设其拥有超级权限）
docker exec -it pg psql -U user -d newsdb

# 执行一次性 SQL：启用扩展(只用执行一次)
CREATE EXTENSION pg_stat_statements;
```

## 验证是否成功

```sh
SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';

SELECTkkkkkkj
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

## 定期查看 top SQL

```sh
CREATE VIEW top_slow_queries AS
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 50;
```

```sh
# 查看
SELECT * FROM top_slow_queries;
```
