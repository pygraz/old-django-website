from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

admin.autodiscover()

urlpatterns = [
    path("", views.index, name="index"),
    # Overwrites for userena
    path("accounts/", include("pygraz_website.apps.accounts.urls")),
    path("accounts/", include("userena.urls")),
    path("meetups/", include("pygraz_website.apps.meetups.urls")),
    path("companies/", include("pygraz_website.apps.companies.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
