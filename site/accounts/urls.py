from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/reset-password.html'),
         name='reset_password'),
    path('reset-password/sent',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/reset-password-done.html'),
         name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/reset-password-confirm.html'),
         name='password_reset_confirm'),
    path('reset-password/success/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/reset-password-complete.html'),
         name='password_reset_complete'),
]
