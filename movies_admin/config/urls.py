"""URL Configuration."""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
        *urlpatterns
    ]
