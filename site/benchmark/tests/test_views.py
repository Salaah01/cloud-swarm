from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from accounts import models as account_models
from sites import models as site_models
from .. import models as benchmark_models


User = get_user_model()


class TestBasicViews(TestCase):
    """Tests simple views that do not have any complex logic and mostly just
    render a template.
    """

    def setUp(self):
        self.account = account_models.Account.objects.get_or_create(
            user=User.objects.get_or_create(
                username='test',
                password='test'
            )[0],
        )[0]
        package = self.account.package_history.first()
        package.quota = 100
        package.save()
        self.site = site_models.Site.objects.get_or_create(
            name='Test Site',
            slug='test-site',
            domain='iamsalaah.com',
            last_verified=timezone.now()
        )[0]
        self.site.add_account(
            self.account, site_models.SiteAccess.AuthLevels.ADMIN)
        self.client = Client()
        self.client.force_login(self.account.user)

    def test_get_new_benchmark_for_site(self):
        response = self.client.get(
            reverse(
                'new_benchmark_for_site',
                args=[self.site.id, self.site.slug]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post_new_benchmark_for_site(self):
        response = self.client.post(
            reverse(
                'new_benchmark_for_site',
                args=[self.site.id, self.site.slug]
            ),
            {
                'requested_by': self.account.id,
                'num_requests': 1,
                'num_servers': 1,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            benchmark_models.Benchmark.objects.count(),
            1,
            list(get_messages(response.wsgi_request))
        )

    def test_get_new_benchmark(self):
        response = self.client.get(reverse('new_benchmark'))
        self.assertEqual(response.status_code, 200)

    def test_post_new_benchmark(self):
        response = self.client.post(
            reverse('new_benchmark'),
            {
                'site': self.site.id,
                'requested_by': self.account.id,
                'num_requests': 1,
                'num_servers': 1,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            benchmark_models.Benchmark.objects.count(),
            1,
            list(get_messages(response.wsgi_request))
        )
