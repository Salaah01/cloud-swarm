from django.http import HttpRequest, HttpResponse
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts import models as account_models
from .. import models as site_models, decorators as site_decorators


User = get_user_model()


def get_request(seed: int) -> RequestFactory:
    """Mimics a get request object. Attaches a user and account to the request
    object.
    """
    user = User.objects.get_or_create(
        username=f'test-{seed}',
        password=f'test-{seed}'
    )[0]
    account = account_models.Account.objects.get(user=user)
    request = RequestFactory().get('/')
    request.user = user
    request.account = account
    return request


class TestRequiredSiteAccess(TestCase):
    """Tests the `required_site_access` decorator."""

    @staticmethod
    def view(
        request: HttpRequest,
        site: site_models.Site,
        site_access: site_models.SiteAccess,
        *args,
        **kwargs
    ) -> HttpResponse:
        """Implements a basic view that will be decorated and will eventually
        be passed the `site` and `site_access` objects.
        """
        return HttpResponse('page accessed')

    def test_site_does_not_exist(self):
        """Test that the decorator returns a 404 if the site does not exist."""
        request = get_request(1)
        response = site_decorators.required_site_access(
            self.view
        )(request, id=1, slug='example')
        self.assertEqual(response.status_code, 404)

    def test_unauthorised_used(self):
        """Test that the decorator returns a 404 if the user is not authorised
        to access the site.
        """
        site = site_models.Site.objects.create(
            name='Example',
            slug='example',
            domain='example.com',
        )
        request = get_request(1)
        response = site_decorators.required_site_access(
            self.view
        )(request, id=site.id, slug='example')
        self.assertEqual(response.status_code, 404)

    def test_authorised_user(self):
        """Test that the decorator returns a 200 if the user is authorised to
        access the site.
        """
        request = get_request(1)
        site = site_models.Site.objects.create(
            name='Example',
            slug='example',
            domain='example.com',
        )
        site.add_account(
            account_models.Account.objects.get(user=request.user),
            0
        )
        response = site_decorators.required_site_access(
            self.view
        )(request, id=site.id, slug='example')
        self.assertEqual(response.status_code, 200)


class RequireVerifiedSite(TestCase):
    """Tests the `require_verified_site` decorator."""

    @staticmethod
    def view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Implements a basic view that will be decorated.
        """
        return HttpResponse('page accessed')

    def test_site_is_none(self):
        """Test that the decorator returns a 404 if the site is None."""
        request = get_request(1)
        response = site_decorators.require_verified_site(
            self.view,
        )(request, site=None)
        self.assertEqual(response.status_code, 404)

    def test_unverified_site(self):
        """Test that the decorator returns a 403 if the site is not verified.
        """
        site = site_models.Site.objects.create(
            name='Example',
            slug='example',
            domain='iamsalaah.com',
        )
        request = get_request(1)
        response = site_decorators.require_verified_site(
            self.view,
        )(request, site=site)
        self.assertEqual(response.status_code, 403)

    def test_verified_site(self):
        """Test that the decorator returns a 200 if the site is verified."""
        site = site_models.Site.objects.create(
            name='Example',
            slug='example',
            domain='iamsalaah.com',
            last_verified=timezone.now(),
        )
        request = get_request(1)
        response = site_decorators.require_verified_site(
            self.view,
        )(request, site=site)
        self.assertEqual(response.status_code, 200)
