release: python3 manage.py makemigrations
release: python3 manage.py migrate
web: gunicorn dataScrapping.wsgi:application --log-file=-
