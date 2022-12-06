# FIXME#40: from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCompaniesView.as_view(), name="list-companies"),
    path("show/<int:pk>/", views.CompanyDetailsView.as_view(), name="company-details"),
    # FIXME#40: Enable company update form.
    # path(
    #     "update/<int:pk>/",
    #     views.UpdateCompanyView.as_view(),
    #     name="update-company",
    # ),
    # FIXME#40: Enable company submission form.
    # path(
    #     "submit/",
    #     views.SubmitCompanyView.as_view(),
    #     name="submit-company",
    # ),
]
