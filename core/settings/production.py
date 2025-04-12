from .base import *  # noqa: F403

# Configuraciones de seguridad para producción
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Example: Database settings override for production if needed
# DATABASES = {
#     'default': {
#         # Production database settings
#     }
# }
