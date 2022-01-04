from django.http import HttpRequest, HttpResponse, JsonResponse
from ..decorators import validate_jwt_payload
from benchmark import models as benchmark_models


@validate_jwt_payload
def benchmark_results(request: HttpRequest, payload: dict) -> HttpResponse:
    """API endpoint for updating the benchmark results."""
    benchmark = benchmark_models.Benchmark.objects.get(
        id=payload['benchmark_id']
    )
    benchmark.min_time = payload['min_time']
    benchmark.max_time = payload['max_time']
    benchmark.mean_time = payload['avg_time']
    benchmark.completed_requests = payload['complete_requests']
    benchmark.failed_requests = payload['failed_requests']
    benchmark.sys_error_requests = payload['sys_error_requests']

    benchmark.save()
    benchmark.progress.set_completed()

    return JsonResponse({'success': True})
