"""Contains functions to communicate with the site API."""

import os
import requests
from jwt_utils import create_jwt

API_DOMAIN = os.getenv('INTERNAL_API_DOMAIN', 'http://localhost:8000')


def send_progress(benchmark_id: int, progress: int) -> None:
    """Sends the progress of a benchmark to the site API.
    Args:
        benchmark_id (int): ID of the benchmark
        progress (int): The progress of the benchmark.
    """
    payload = {
        'benchmark_id': benchmark_id,
        'status': progress
    }
    token = create_jwt(payload)
    requests.post(
        F'{API_DOMAIN}/internal-api/benchmark-progress/',
        json={'token': token}
    )


def send_results(
    benchmark_id: int,
    min_time: int,
    max_time: int,
    mean_time: int,
    completed_requests: int,
    failed_requests: int
) -> None:
    """Sends the results of a benchmark to the site API.
    Args:
        benchmark_id (int): ID of the benchmark
        min_time (int): The minimum time of the benchmark.
        max_time (int): The maximum time of the benchmark.
        mean_time (int): The mean time of the benchmark.
        completed_requests (int): The number of completed requests.
        failed_requests (int): The number of failed requests.
    """
    payload = {
        'benchmark_id': benchmark_id,
        'min_time': min_time,
        'max_time': max_time,
        'avg_time': mean_time,
        'complete_requests': completed_requests,
        'failed_requests': failed_requests
    }
    token = create_jwt(payload)
    requests.post(
        F'{API_DOMAIN}/internal-api/benchmark-results/',
        json={'token': token}
    )
