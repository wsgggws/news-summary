# PG 版本升级

pg 13.0 => pg 16.0

## 准备 postgres image(ECS 上可能拉取不了)

```ssh
# 我本地能拉取使用，打包
docker save postgres:16 -o postgres16.tar

scp postgres16.tar RSS:~/

# 登录服务器
ssh RSS

# 加载
docker load -i ~/postgres16.tar

# 验证
docker images

# 强制清理旧网络并重新创建, 避免尝试连接一个 不存在或已损坏的网络
docker network prune -f

```

## 修改 docker-compose.yml

`image: postgres:16`

## 备份原有数据库数据（重要）

```sh
docker exec -t pg pg_dumpall -U user > all_backup.sql
```

## 升级数据目录

- 删除旧 volume 数据目录（确保你有备份, !!!并查看备份文件的内容是不是正确的）
  `cat all_backup.sql`
  `rm -rf ./data/postgres`
- 重新创建容器并初始化空数据库
  `docker-compose up -d --build db`
- 还原数据

  ```sh
  # 先保存原文件内容到临时文件
  cp all_backup.sql all_backup.sql.bak

  # 新建文件，把两行写进去，再把原内容追加(这是由于web启动时自动创建了新表)
  {
    echo "DROP SCHEMA public CASCADE;"
    echo "CREATE SCHEMA public;"
    cat all_backup.sql.bak
  } > all_backup.sql

  # !!! 再次查看是不是内容正确的
  cat all_backup.sql

  cat all_backup.sql | docker exec -i pg psql -U user -d newsdb
  ```

- 验证升级是否成功
  `docker exec -it pg psql -U user -d newsdb -c "SELECT version();"`

- 重设用户密码（生成 SCRAM 密码, pg13使用 md5, 也可以修改 pg_hba.conf）

```sh
docker exec -it pg psql -U user -d newsdb
ALTER USER "user" WITH PASSWORD 'password';
```

options (change pg_hba.conf)

```text
host all all all scram-sha-256

# =>

host all all all md5

```

- 再次重启
  `make docker-run`
