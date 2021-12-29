from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:id>-<slug:slug>/', views.site, name='site'),
    path('new/', views.NewSite.as_view(), name='new_site'),
]
