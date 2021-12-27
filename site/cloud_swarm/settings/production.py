import os
from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = []

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
PREPEND_WWW = True

MIDDLEWARE += [  # noqa: F405
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware'
]

CACHE_TTL = None
CAPTCHA_TEST_MODE = False
