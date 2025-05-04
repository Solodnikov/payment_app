# payment_app


### check

python manage.py makemigrations

python manage.py migrate

python manage.py runserver


### create superuser
python manage.py createsuperuser


### celery
для Windows
celery -A celery_app worker --loglevel=info -P solo

Unix
celery -A celery_app worker --loglevel=info

### redis
docker run -d -p 6379:6379 redis
docker run -d --name redis -p 6379:6379 redis