from django.urls import path
from . import views

site_uri = '<int:id>-<slug:slug>'

urlpatterns = [
    path(
        f'{site_uri}/new/',
        views.NewBenchmark.as_view(),
        name='new_benchmark'
    ),
]
