from django.contrib import admin
from . import models


class SiteAccessInline(admin.TabularInline):
    model = models.SiteAccess
    extra = 0


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'txt_record', 'last_benchmarked',
                    'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'domain')
    ordering = ('-created_on', 'name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SiteAccessInline]


@admin.register(models.VerificationCheckLog)
class VerificationCheckLogAdmin(admin.ModelAdmin):
    list_display = ('site', 'created_on', 'account')
    list_filter = ('created_on',)
    search_fields = ('site__name', 'site__domain', 'account__user__username')
    ordering = ('-created_on',)
