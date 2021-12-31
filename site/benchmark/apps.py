from django.apps import AppConfig


class BenchmarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'benchmark'

    def ready(self):
        # import all signal handlers
        from . import signals  # noqa F401
