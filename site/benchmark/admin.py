from django.contrib import admin
from . import models


class BenchmarkProgressInline(admin.TabularInline):
    model = models.BenchmarkProgress
    extra = 0


@admin.register(models.Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = (
        'site',
        'requested_by',
        'created_on',
        'num_servers',
        'num_requests',
        'started_on',
        'scheduled_on',
        'completed_on',
        'sys_error_requests'
    )
    readonly_fields = ('created_on',)
    fieldsets = (
        (None, {
            'fields': (
                'site',
                'requested_by',
            )
        }),
        ('Dates', {
            'fields': (
                'created_on',
                'started_on',
                'scheduled_on',
                'completed_on',
            )
        }),
        ('Benchmark Paramaters', {
            'fields': (
                'num_servers',
                'num_requests',
            )
        }),
        ('Results', {
            'fields': (
                'min_time',
                'max_time',
                'mean_time',
                'completed_requests',
                'failed_requests',
                'sys_error_requests',
            )
        }),
    )
    inlines = [BenchmarkProgressInline]
