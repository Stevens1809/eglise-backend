release: python manage.py migrate && python manage.py seed_data
web: gunicorn config.wsgi --log-file -
