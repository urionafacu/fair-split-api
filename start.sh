#!/bin/bash

# Aplicar migraciones
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2
