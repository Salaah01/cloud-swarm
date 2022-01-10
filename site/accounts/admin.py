from django.contrib import admin
from . import models


class PackageHistoryInline(admin.TabularInline):
    """Inline for PackageHistory."""

    model = models.PackageHistory
    extra = 0


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'package',
        'expiry_date',
        'refresh_period_end_on',
        'remaining_quota',
    )
    raw_id_fields = ('user',)
    inlines = (PackageHistoryInline,)
