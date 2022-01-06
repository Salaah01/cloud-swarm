from django.conf import settings


def root_domain(request):
    """Returns the root domain of the bluish_pink app."""
    return {
        'ROOT_DOMAIN': settings.ROOT_DOMAIN,
        'SITE_NAME': settings.SITE_NAME,
        'SOCIAL': settings.SOCIAL,
    }
