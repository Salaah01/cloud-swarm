"""Helper methods for the unittests, these predominately are functions to
create model instances.
"""
from typing import Optional
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.contrib.auth import models as auth_models

# Auth


def simple_request() -> RequestFactory:
    request = RequestFactory()
    request.user = auth_models.AnonymousUser()
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    return request


def simple_get_response(path: str = '/') -> HttpResponse:
    return Client().get(path)


def get_user(seed: Optional[int] = 1) -> auth_models.User:
    return auth_models.User.objects.get_or_create(
        username=f'test-{seed}@test.com',
        email=f'test-{seed}@test.com',
        password='password',
        first_name='first name',
        last_name='last name',
    )[0]
