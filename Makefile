ARGS ?=

# 告诉 make 这三个名字不是文件名，而是“伪目标”（phony targets）。
.PHONY: run test otel-run celery-run

# @ 前缀：让这个命令在执行时不打印命令本身，只输出脚本中的 echo 和结果，保持输出干净。
run:
	@./scripts/dev.sh

test:
	@./scripts/test.sh $(ARGS)

otel-run:
	@./scripts/otel-run.sh

celery-run:
	@./scripts/celery-run.sh
