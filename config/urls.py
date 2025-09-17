# config/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # API Endpoints
    path("api/accounts/", include("accounts.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),  # Revert to the standard include
    path("api/observations/", include("observations.urls")),
    path("api/", include("clustering.urls")),
    path("api/", include("scan_periods.urls")),
    # Frontend Pages
    path("", include("core.urls")),
    path("report/", include("reporting.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
