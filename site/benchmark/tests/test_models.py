import typing as _t
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts import models as account_models
from sites import models as site_models
from .. import models as benchmark_models


User = get_user_model()


def get_account(seed: int = 1) -> User:
    """Return a user with the given seed."""
    user = User.objects.get_or_create(
        username=f'User {seed}',
        password='password',
    )[0]
    return account_models.Account.objects.get(user=user)


def get_site(seed: int = 1) -> site_models.Site:
    """Return a site with the given seed."""
    return site_models.Site.objects.get_or_create(
        name=f'Site {seed}',
        domain=f'example-{seed}.com',
    )[0]


def get_benchmark(
    seed: int = 1,
    site: _t.Optional[site_models.Site] = None,
    account: _t.Optional[account_models.Account] = None,
) -> benchmark_models.Benchmark:
    """Return a benchmark with the given seed."""
    return benchmark_models.Benchmark.objects.get_or_create(
        site=site or get_site(seed),
        requested_by=account or get_account(seed),
    )[0]


def get_benchmark_progress(
    seed: int = 1,
    benchmark: _t.Optional[benchmark_models.Benchmark] = None,
    status: _t.Optional[benchmark_models.BenchmarkProgress.StatusChoices] = None,  # noqa: E501
) -> benchmark_models.BenchmarkProgress:
    """Return a benchmark progress with the given seed."""
    return benchmark_models.BenchmarkProgress.objects.get_or_create(
        benchmark=benchmark or get_benchmark(seed),
        status=status or benchmark_models.BenchmarkProgress.StatusChoices.PENDING,  # noqa: E501
    )[0]


class TestBenchmark(TestCase):

    def test__str__(self):
        self.assertIsInstance(str(get_benchmark()), str)

    def test_for_site(self):
        site_1 = get_site()
        site_2 = get_site(2)
        get_benchmark(site=site_1)
        get_benchmark(seed=2, site=site_1)
        get_benchmark(site=site_2)

        results = benchmark_models.Benchmark.for_site(site_1)
        self.assertEqual(results.count(), 2)

    def test_for_account(self):
        account_1 = get_account()
        account_2 = get_account(2)
        get_benchmark(account=account_1)
        get_benchmark(seed=2, account=account_1)
        get_benchmark(account=account_2)

        results = benchmark_models.Benchmark.for_account(account_1)
        self.assertEqual(results.count(), 2)

    def test_not_started(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.started_on = None
        benchmark_1.save()
        benchmark_2.started_on = timezone.now()
        benchmark_2.save()

        results = benchmark_models.Benchmark.not_started()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_started(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.started_on = timezone.now()
        benchmark_1.save()
        benchmark_2.started_on = None
        benchmark_2.save()

        results = benchmark_models.Benchmark.started()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_scheduled(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.scheduled_on = timezone.now()
        benchmark_1.save()
        benchmark_2.scheduled_on = None
        benchmark_2.save()

        results = benchmark_models.Benchmark.scheduled()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_not_scheduled(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.scheduled_on = None
        benchmark_1.save()
        benchmark_2.scheduled_on = timezone.now()
        benchmark_2.save()

        results = benchmark_models.Benchmark.not_scheduled()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_completed(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.completed_on = timezone.now()
        benchmark_1.save()
        benchmark_2.completed_on = None
        benchmark_2.save()

        results = benchmark_models.Benchmark.completed()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_not_completed(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)

        benchmark_1.completed_on = None
        benchmark_1.save()
        benchmark_2.completed_on = timezone.now()
        benchmark_2.save()

        results = benchmark_models.Benchmark.not_completed()
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0], benchmark_1)

    def test_avg_completion_time(self):
        benchmark_1 = get_benchmark()
        benchmark_2 = get_benchmark(2)
        benchmark_3 = get_benchmark(3)

        benchmark_1.completed_on = None
        benchmark_1.save()

        now = timezone.now()

        benchmark_2.started_on = now - timedelta(seconds=5)
        benchmark_2.completed_on = now
        benchmark_2.save()

        benchmark_3.started_on = now - timedelta(seconds=9)
        benchmark_3.completed_on = now
        benchmark_3.save()

        results = benchmark_models.Benchmark.avg_completion_time()
        self.assertEqual(results, timedelta(seconds=7))


class BenchmarkProgress(TestCase):

    def test__str__(self):
        self.assertIsInstance(str(get_benchmark_progress()), str)

    def test_set_completed(self):
        benchmark_progress = get_benchmark_progress()
        benchmark_progress.set_completed()
        self.assertIsNotNone(
            benchmark_progress.benchmark.site.last_benchmarked
        )
        self.assertEqual(
            benchmark_progress.status,
            benchmark_models.BenchmarkProgress.StatusChoices.COMPLETED
        )
