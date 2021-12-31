"""Contains methods to send messages to the event bus."""

import json
import redis
from django.conf import settings
from . import models as benchmark_models

_connection = redis.Redis(**settings.EVENT_BUS)


def publish_message(channel: str, message: dict) -> None:
    """Publish a message to the event bus.
    Args:
        channel: The channel to publish to.
        message: The message to publish.
    """
    _connection.publish(channel, json.dumps(message))


def new_benchmark(benchmark: benchmark_models.Benchmark) -> None:
    """Publish a new benchmark to the event bus.
    Args:
        benchmark: The benchmark to publish.
    """
    publish_message(
        'benchmark.new',
        {
            'id': benchmark.id,
            'domain': benchmark.site.domain,
            'num_servers': benchmark.num_servers,
            'num_requests': benchmark.num_requests,
        }
    )
