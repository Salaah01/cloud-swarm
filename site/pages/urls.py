from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pricing/', views.prices, name='prices'),
    path(
        'docs/',
        include(([
            path('', views.docs.index, name='index'),
        ], 'docs'), namespace='docs'),
    ),
    path(
        'terms-and-conditions/',
        views.terms_and_conditions,
        name='terms_and_conditions'
    ),
]
