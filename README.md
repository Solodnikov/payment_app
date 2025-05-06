# payment_app

### check

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

daphne -b 0.0.0.0 -p 8000 core.asgi:application

### create superuser
python manage.py createsuperuser


### celery
для Windows
celery -A core.celery_app worker --loglevel=info -P solo

Unix
celery -A core.celery_app worker --loglevel=info

### redis
docker run -d --name redis -p 6379:6379 redis