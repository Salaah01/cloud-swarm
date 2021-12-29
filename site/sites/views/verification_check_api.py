from django.http import HttpRequest, JsonResponse
from django.conf import settings
from ..decorators import required_site_access
from .. import models as site_models


@required_site_access
def verification_check_api(
    request: HttpRequest,
    site: site_models.Site,
    site_access: site_models.SiteAccess
) -> JsonResponse:
    """API endpoint for checking if a site is verified.
    Args:
        request (HttpRequest): The request object.
        site (site_models.Site): The site object.
        site_access (site_models.SiteAccess): The site access object.
    """

    # Prevent the user from verifying a site too frequently.
    if not site_models.VerificationCheckLog.can_run_check(site):
        return JsonResponse({
            'success': False,
            'message': 'A verification check was done recently. Please wait '
            f'{settings.SITES_VERIFY_TIMEOUT_SECS} between '
            'requests.'
        })

    site_models.VerificationCheckLog.add_log(site, request.user)

    return JsonResponse({
        'success': True,
        'data': {
            'verified': site.verify(),
            'txt_record': site.txt_record
        }
    })
