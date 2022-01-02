import time
from django.http import HttpRequest, HttpResponse, JsonResponse
from ..decorators import validate_jwt_payload
from benchmark import models as benchmark_models


@validate_jwt_payload
def benchmark_progress(request: HttpRequest, payload: dict) -> HttpResponse:
    """API endpoint for updating the database with the progress of a benchmark.
    """
    try:
        benchmark = benchmark_models.Benchmark.objects.get(
            id=payload['benchmark_id']
        )
    except benchmark_models.Benchmark.DoesNotExist:
        # It is possible that the benchmark record is not yet created, so we
        # can wait a few seconds and try again.
        time.sleep(5)
        benchmark = benchmark_models.Benchmark.objects.get(
            id=payload['benchmark_id']
        )

    progress = benchmark.progress
    progress.status = payload['status']
    progress.save()
    return JsonResponse({'success': True})
