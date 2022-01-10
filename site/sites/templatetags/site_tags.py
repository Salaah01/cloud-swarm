from django import template
from accounts.models import Account
from .. import models as site_models

register = template.Library()


@register.simple_tag
def has_benchmark_privileges(account: Account, site: site_models.Site) -> bool:
    """Returns whether the user can benchmark the site."""
    account_access = site_models.SiteAccess.account_access(site, account)
    if not account_access:
        return False
    return account_access.account_has_auth(
        site_models.SiteAccess.AuthLevels.MANAGER
    )
