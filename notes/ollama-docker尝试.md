# ollama-docker-compose 部署尝试

复制如下内容到 docker-compose 里，使用 `docker-compose up -d ollama` 即可

```yml
ollama-init:
  image: ollama/ollama
  container_name: ollama-init
  entrypoint: ["sh", "-c"]
  # command: ["ollama serve & sleep 3 && ollama pull llama3:8b"]
  # command: ["ollama serve & sleep 3 && ollama pull tinyllama"]
  # command: ["ollama serve & sleep 3 && ollama pull gemma2:2b"]
  command: ["ollama serve & sleep 3 && ollama pull qwen:1.8b"]
  volumes:
    - ollama_data:/root/.ollama
  environment:
    - OLLAMA_MODELS=/root/.ollama
  networks:
    - otel-net
  restart: "no"
ollama:
  image: ollama/ollama
  container_name: ollama
  depends_on:
    ollama-init:
      condition: service_completed_successfully
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
  environment:
    - OLLAMA_MODELS=/root/.ollama
  restart: unless-stopped
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:11434"]
    interval: 30s
    timeout: 10s
    retries: 5
    start_period: 10s
  networks:
    - otel-net

volumes:
  ollama_data:
```
