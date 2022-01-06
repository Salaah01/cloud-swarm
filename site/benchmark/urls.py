from django.urls import path
from . import views

site_uri = '<int:id>-<slug:slug>'

urlpatterns = [
    path(
        f'new/{site_uri}/',
        views.NewBenchmarkForSite.as_view(),
        name='new_benchmark_for_site'
    ),
    path('new/', views.NewBenchmark.as_view(), name='new_benchmark'),
]
