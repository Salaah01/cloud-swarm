"""Site map for the accounts app."""

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class AccountsStaticSitemap(Sitemap):
    """Site map for the accounts app."""
    protocol = "https"

    def items(self):
        return ['login', 'register']

    def location(self, item):
        return reverse(item)
