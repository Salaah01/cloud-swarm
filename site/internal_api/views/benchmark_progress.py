from django.http import HttpRequest, HttpResponse, JsonResponse
from ..decorators import validate_jwt_payload
from benchmark import models as benchmark_models


@validate_jwt_payload
def benchmark_progress(request: HttpRequest, payload: dict) -> HttpResponse:
    """API endpoint for updating the database with the progress of a benchmark.
    """

    print('\033[92m', payload, '\033[0m')

    benchmark = benchmark_models.Benchmark.objects.get(
        id=payload['benchmark_id']
    )
    progress = benchmark.progress
    progress.status = payload['status']
    progress.save()
    return JsonResponse({'success': True})
