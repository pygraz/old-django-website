from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^$', views.ListCompaniesView.as_view(), name='list-companies'),
    url(r'^show/(?P<pk>\d+)/$', views.CompanyDetailsView.as_view(),
        name='company-details'),
    url(r'^update/(?P<pk>\d+)/$', login_required(
        views.UpdateCompanyView.as_view()),
        name='update-company'),
    url(r'^submit/$', login_required(views.SubmitCompanyView.as_view()),
        name='submit-company')
)
