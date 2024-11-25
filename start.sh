#!/bin/bash
# Apply migrations
python manage.py migrate

# Init Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2
