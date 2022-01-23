from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class TestUrls(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view."""

    def test_dashboard(self):
        self.assertEquals(
            resolve(reverse('sites-dashboard')).func,
            views.dashboard
        )

    def test_site(self):
        self.assertEquals(
            resolve(reverse('site', args=[1, 'test-site'])).func,
            views.site
        )

    def test_new_site(self):
        self.assertEquals(
            resolve(reverse('new_site')).func.view_class,
            views.NewSite
        )

    def test_verification_check_api(self):
        self.assertEquals(
            resolve(reverse(
                'verification_check_api',
                args=[1, 'test-site']
            )).func,
            views.verification_check_api
        )
