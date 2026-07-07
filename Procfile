release: python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_data
web: gunicorn config.wsgi --log-file -