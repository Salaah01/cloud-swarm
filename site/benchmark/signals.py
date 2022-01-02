from django.db import models
from django.utils import timezone
from . import producer as benchmark_producer
from . import models as benchmark_models


def on_new_benchmark(
    sender: models.Model,
    instance: benchmark_models.Benchmark,
    **kwargs
) -> None:
    """Publish a new benchmark to the event bus and created a benchmark
    progress record.

    Args:
        instance: The benchmark to publish.
    """
    benchmark_models.BenchmarkProgress.objects.create(
        benchmark=instance
    ).save()
    benchmark_producer.new_benchmark(instance)


def on_benchmark_progress_update(
    sender: models.Model,
    instance: benchmark_models.BenchmarkProgress,
    **kwargs
) -> None:
    status_choices = benchmark_models.BenchmarkProgress.StatusChoices
    loggable_statues = (
        status_choices.PROVISIONING,
        status_choices.SCHEDULING,
        status_choices.COMPLETED,
    )
    if instance.status not in loggable_statues:
        return
    if instance.status == status_choices.PROVISIONING:
        instance.benchmark.started_on = timezone.now()
    elif instance.status == status_choices.SCHEDULING:
        instance.benchmark.scheduled_on = timezone.now()
    elif instance.status == status_choices.COMPLETED:
        instance.benchmark.completed_on = timezone.now()
    instance.benchmark.save()


benchmark_models.NEW_BENCHMARK.connect(
    on_new_benchmark,
    benchmark_models.Benchmark
)

benchmark_models.UPDATED_BENCHMARK_PROGRESS.connect(
    on_benchmark_progress_update,
    benchmark_models.BenchmarkProgress
)
