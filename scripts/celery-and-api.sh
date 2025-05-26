nohup python3.11 -m celery -A celery_app beat --loglevel=info 2>&1 &

nohup python3.11 -m celery -A celery_app worker --hostname=worker1 --pool=threads --concurrency=1 --loglevel=info 2>&1 &
nohup python3.11 -m celery -A celery_app worker --hostname=worker2 --pool=threads --concurrency=1 --loglevel=info 2>&1 &

uvicorn app.main:app --host 0.0.0.0 --port 8000
