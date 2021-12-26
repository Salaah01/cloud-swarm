from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'Web Horde Admin'
admin.site.site_title = 'Web Horde Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]

# Static Files
urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
