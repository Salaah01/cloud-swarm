from typing import Union
from django.http import HttpRequest
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    validate_password as dj_validate_password
)
from django.core.validators import validate_email as dj_validate_email
from django.core.exceptions import ValidationError
from core_functions import dataclasses


def validate_email(email: str) -> bool:
    """Validates an `email` to check that is in the correct format. Returns a
    `bool` representing whether or not it has passed the validation.
    """
    try:
        dj_validate_email(email)
        return True
    except ValidationError:
        return False


def login_user(
    request: HttpRequest,
    email: str,
    password: str
) -> Union[User, None]:
    """Attempts to login a user returning the user object if authentication
    was successful.
    """
    if not validate_email(email):
        return None

    user = auth.authenticate(username=email, password=password)
    if not user:
        return None

    auth.login(
        request,
        user,
        backend='django.contrib.auth.backends.ModelBackend'
    )

    return user


def validate_password(password: str) -> (bool, str):
    """Validates a password.

    Args:
        password - (str) Password to validate.
    Returns:
        bool - Represents where the password is valid.
        str - Reason validation failed.
    """
    try:
        dj_validate_password(password)
        return (True, '')
    except ValidationError as err:
        return (False, err.error_list[0].message)


def sign_up_user(
    request: HttpRequest,
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    confirm_password: str
) -> dataclasses.APIResponse:
    """Attempts to sign up the user retuning the user object if sign up is
    successful.
    """

    # Validation
    email_validation = validate_email(email)
    if not email_validation:
        return dataclasses.APIResponse(
            success=False,
            error_type='Invalid email',
            error='This is an invalid email.'
        )

    # Check if the email address is already in use.
    if User.objects.filter(email=email).exists():
        return dataclasses.APIResponse(
            success=False,
            error_type='Email exists',
            error='This email address already exists.'
        )

    if not all([first_name, last_name, password, confirm_password]):
        return dataclasses.APIResponse(
            success=False,
            error_type='Missing field(s)',
            error='Not all required fields have been filed in.'
        )

    if password != confirm_password:
        return dataclasses.APIResponse(
            success=False,
            error_type='Passwords do not match',
            error='Passwords do not match.'
        )

    password_validation = validate_password(password)
    if not validate_password(password):
        return dataclasses.APIResponse(
            success=False,
            error_type='Insecure password',
            error=password_validation[1]
        )

    # Register and login user
    user = User.objects.create_user(
        username=email,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    user.save()
    auth.login(
        request,
        user,
        backend='django.contrib.auth.backends.ModelBackend'
    )

    return dataclasses.APIResponse(
        success=True,
        retuned_object=user
    )
