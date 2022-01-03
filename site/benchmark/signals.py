from django.db import models
from django.utils import timezone
from . import producer as benchmark_producer
from . import models as benchmark_models
from . import consumers as benchmark_consumers


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

    # Update the benchmark time logs.
    loggable_statues = (
        status_choices.PROVISIONING,
        status_choices.SCHEDULING,
        status_choices.COMPLETED,
    )
    if instance.status not in loggable_statues:
        pass
    if instance.status == status_choices.PROVISIONING:
        instance.benchmark.started_on = timezone.now()
    elif instance.status == status_choices.SCHEDULING:
        instance.benchmark.scheduled_on = timezone.now()
    elif instance.status == status_choices.COMPLETED:
        instance.benchmark.completed_on = timezone.now()
    instance.benchmark.save()

    # Send notification with new status.
    benchmark_consumers.BenchmarkProgressConsumer.send_status_update(
        instance.benchmark.site_id,
        instance.benchmark_id,
        instance.get_status_display(),
        instance.benchmark.scheduled_on,
    )


benchmark_models.NEW_BENCHMARK.connect(
    on_new_benchmark,
    benchmark_models.Benchmark
)

benchmark_models.UPDATED_BENCHMARK_PROGRESS.connect(
    on_benchmark_progress_update,
    benchmark_models.BenchmarkProgress
)
