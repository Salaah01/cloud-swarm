from django.urls import path
from . import views

urlpatterns = [
    path(
        'benchmark-progress/',
        views.benchmark_progress,
        name='benchmark_progress'
    ),
    path(
        'benchmark-results/',
        views.benchmark_results,
        name='benchmark_results'
    ),
]
