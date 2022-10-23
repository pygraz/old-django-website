from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from . import views


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Overwrites for userena
    url(r'^accounts/', include('pygraz_website.apps.accounts.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^meetups/', include('pygraz_website.apps.meetups.urls')),
    url(r'^companies/', include('pygraz_website.apps.companies.urls')),
    url("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
