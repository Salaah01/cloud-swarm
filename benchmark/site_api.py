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
