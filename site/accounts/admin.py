from django.contrib import admin
from . import models


class BillingAddressInline(admin.StackedInline):
    model = models.BillingAddress
    extra = 0


class PackageHistoryInline(admin.TabularInline):
    model = models.PackageHistory
    extra = 0


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'package',
        'expiry_date',
        'remaining_quota',
    )
    raw_id_fields = ('user',)
    inlines = (
        BillingAddressInline,
        PackageHistoryInline,
    )
