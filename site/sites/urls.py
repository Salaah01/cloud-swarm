from django.urls import path
from . import views

site_uri = '<int:id>-<slug:slug>'

urlpatterns = [
    path('', views.dashboard, name='sites-dashboard'),
    path(f'{site_uri}/', views.site, name='site'),
    path('new/', views.NewSite.as_view(), name='new_site'),
    path(f'{site_uri}/verification-check/', views.verification_check_api,
         name='verification_check_api'),
]
