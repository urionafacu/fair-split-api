from .base import *  # noqa: F403

# Security settings for production
DEBUG = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Define explicit allowed hosts for production
ALLOWED_HOSTS = [
    "localhost",
    "fair-split-api-production.up.railway.app",
]

# CSRF trusted origins (add your production domains)
CSRF_TRUSTED_ORIGINS = ["https://fair-split-api-production.up.railway.app"]
