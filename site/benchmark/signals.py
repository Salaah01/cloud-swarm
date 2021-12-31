from django.db import models
from . import producer as benchmark_producer
from . import models as benchmark_models


def on_new_benchmark(
    sender: models.Model,
    instance: benchmark_models.Benchmark,
    **kwargs
) -> None:
    """Publish a new benchmark to the event bus.

    Args:
        instance: The benchmark to publish.
    """
    benchmark_producer.new_benchmark(instance)


benchmark_models.NEW_BENCHMARK.connect(
    on_new_benchmark,
    benchmark_models.Benchmark
)
