from .base import *  # noqa: F403

DEBUG = True

# Test-specific settings
# Example: Use an in-memory database for tests
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_fairsplit",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
        "TEST": {
            "NAME": "test_fairsplit",
            "SERIALIZE": False,
        },
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Allow requests from local development origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4000",
    "http://127.0.0.1:4000",
    # Add other origins if needed, e.g., frontend if it posts directly
]
