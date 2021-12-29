from django.http import HttpRequest, JsonResponse
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
            'message': 'A verification check was done recently. Please wait a while longer before trying again.'  # noqa E501
        })

    site_models.VerificationCheckLog.add_log(site, request.user)

    return JsonResponse({
        'success': True,
        'data': {
            'verified': site.verified,
            'txt_record': site.txt_record
        }
    })
