from django.http import HttpResponse


def terms_and_conditions(request):
    """View for the terms and conditions."""
    return HttpResponse('Terms and conditions.')
