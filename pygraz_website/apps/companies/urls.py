from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListCompaniesView.as_view(), name="list-companies"),
    path("show/<int:pk>/", views.CompanyDetailsView.as_view(), name="company-details"),
    path(
        "update/<int:pk>/",
        login_required(views.UpdateCompanyView.as_view()),
        name="update-company",
    ),
    path(
        "submit/",
        login_required(views.SubmitCompanyView.as_view()),
        name="submit-company",
    ),
]
