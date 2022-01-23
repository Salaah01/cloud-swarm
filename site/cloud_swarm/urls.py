from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

admin.site.site_header = 'Web Horde Admin'
admin.site.site_title = 'Web Horde Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('sites/', include('sites.urls')),
    path('benchmark/', include('benchmark.urls')),
    path('internal-api/', include('internal_api.urls')),
    path('payments/', include('payments.urls')),
]

# Static Files
urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
