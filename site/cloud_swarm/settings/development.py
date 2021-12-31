import sys
from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache
if 'test' in sys.argv:
    CACHE_TTL = 0
    for cache_name in CACHES.keys():  # noqa: F405
        CACHES[cache_name]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'  # noqa: E501,F405
else:
    CACHE_TTL = 60

# This setting allows reCaptcha to always automatically pass when testing the
# application.
if 'test' in sys.argv:
    CAPTCHA_TEST_MODE = True
else:
    CAPTCHA_TEST_MODE = False

INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]

# Enabling template debug option for coverage tests.
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://localhost']
