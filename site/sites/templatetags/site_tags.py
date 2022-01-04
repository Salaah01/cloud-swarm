from django import template
from django.contrib.auth.models import User
from .. import models as site_models

register = template.Library()


@register.simple_tag
def user_can_benchmark(user: User, site: site_models.Site) -> bool:
    """Returns whether the user can benchmark the site."""
    user_access = site_models.SiteAccess.user_access(site, user)
    if not user_access:
        return False
    return user_access.user_has_auth(site_models.SiteAccess.AuthLevels.MANAGER)
