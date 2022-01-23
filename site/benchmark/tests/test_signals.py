from django.test import TestCase
from .. import models as benchmark_models
from .test_models import get_benchmark


class TestOnNewBenchmark(TestCase):
    """Tests the `on_new_benchmark` signal."""

    def test_creates_benchmark_progress(self):
        """Tests that when a new benchmark is created, it created a
        `BenchmarkProgress` record.
        """
        benchmark = get_benchmark()
        self.assertEqual(benchmark_models.BenchmarkProgress.objects.count(), 1)
        self.assertEqual(
            benchmark_models.BenchmarkProgress.objects.first().benchmark,
            benchmark
        )


class TestOnBenchmarkProgressUpdate(TestCase):
    """Tests the `on_benchmark_progress_update` signal."""

    def test_updates_benchmark_progress(self):
        """Tests that when a benchmark progress is updated, it updates the
        benchmark datetime fields.
        """
        benchmark = get_benchmark()
        benchmark_progress = benchmark_models.BenchmarkProgress.objects.get(
            benchmark=benchmark
        )
        status_choices = benchmark_models.BenchmarkProgress.StatusChoices
        benchmark_progress.status = status_choices.PROVISIONING
        benchmark_progress.save()

        self.assertIsNotNone(get_benchmark().started_on)

        benchmark_progress.status = status_choices.SCHEDULING
        benchmark_progress.save()

        self.assertIsNotNone(get_benchmark().scheduled_on)

        benchmark_progress.status = status_choices.COMPLETED
        benchmark_progress.save()

        self.assertIsNotNone(get_benchmark().completed_on)
