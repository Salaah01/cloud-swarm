from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class TestUrls(SimpleTestCase):
    """Unittest to check that the urls resolve the correct view."""

    def test_new_benchmark_for_site(self):
        self.assertEquals(
            resolve(reverse('new_benchmark_for_site',
                    args=[1, 'test-site'])).func.view_class,
            views.NewBenchmarkForSite
        )

    def test_new_benchmark(self):
        self.assertEquals(
            resolve(reverse('new_benchmark')).func.view_class,
            views.NewBenchmark
        )
