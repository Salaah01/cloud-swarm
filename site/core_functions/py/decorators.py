"""Decorators."""

from typing import Iterable
import functools
from django.http import HttpResponseForbidden
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.mixins import UserPassesTestMixin


def _get_request_from_args(args: Iterable) -> WSGIRequest:
    """Helper function to retrive the request object from a list of args."""
    for arg in args:
        if isinstance(arg, WSGIRequest):
            return arg


def supervisor_required(fn=None, *args, **kwargs):
    """Decorater where if the user is not a supervisor, then return a 404
    response.
    """
    def decorate(fn, *args, **kwargs):
        @functools.wraps(fn)
        def _wrapped_view(*args, **kwargs):
            request = _get_request_from_args(args)
            if not request.user.is_superuser:
                return HttpResponseForbidden()

            return fn(*args, **kwargs)

        return _wrapped_view

    return decorate(fn, *args, **kwargs)


def superuser_required_cbv():
    """Decorator for class based views where the user must be a superuser."""
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper
