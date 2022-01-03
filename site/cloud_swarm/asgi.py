"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from benchmark import consumers as benchmark_consumers

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'cloud_swarm.settings.production'
)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path(
                'ws/benchmark-progress/site/<int:site_id>/',
                benchmark_consumers.BenchmarkProgressConsumer.as_asgi()
            ),
        ])
    ),
})
