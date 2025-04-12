from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Configuraciones específicas de desarrollo
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECRET_KEY = "localkey"
