# PG 数据迁移

最佳是在一开始的时候使用主机目录

## old

postgres_data 是命名 volume, 重建时可自动挂载，但如果你迁移主机、清空 Docker，数据会丢失

```yml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

## target

挂载到宿主机目录（可见、可备份）

```yml
volumes:
  - ./data/postgres:/var/lib/postgresql/data
```

## 过程

1. 创建主机目录
   `mkdir -p ./data/postgres`

2. volume 数据导出

   你之所以看到 news-summary_postgres_data 而不是你写的 postgres_data，是因为：
   Docker Compose 默认会在资源名（容器、网络、卷等）前加上项目名作为前缀。
   如需完全控制命名，可以使用 -p 参数或显式声明 external: true

   ```sh
   # 查看有哪些 volume, 需要注意你部署所在的目录
   docker volume ls

   docker run --rm \
     -v news-summary_postgres_data:/from \
     -v $(pwd)/data:/to \
     alpine \
     sh -c "mkdir -p /to/postgres && cd /from && tar cf - . | tar xf - -C /to/postgres"
   ```

3. 确认
   `ls ./data/postgres`

4. 删除旧容器并重建使用新挂载

   ```sh
   make docker-run
   ```
