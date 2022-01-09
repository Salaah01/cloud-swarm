from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'package',
        'expiry_date',
    )
    raw_id_fields = ('user',)


@admin.register(models.PackageHistory)
class PackageHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'account',
        'package',
        'created_on',
        'expiry_date',
    )
    raw_id_fields = ('account',)
