from django.contrib import admin
from . import models


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'one_time_package',
        'instances',
        'requests',
        'refresh_period',
        'quota',
    )
