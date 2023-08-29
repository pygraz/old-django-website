from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from guardian.shortcuts import assign_perm

from . import models


class CompanyTestsMixin:
    def setUp(self):
        self.approved = models.Company(
            name="Approved",
            website="http://company.com",
            address_line="address",
            postal_code="8010",
            city="Graz",
            country="AT",
            approved=True,
        )
        self.approved.save()

        self.user = User.objects.create_user(username="username", password="password", email="test@test.com")

        self.not_approved = models.Company(
            name="Not-Approved",
            website="http://company.com",
            address_line="address",
            postal_code="8010",
            city="Graz",
            country="AT",
            approved=False,
        )
        self.not_approved.save()
        self.not_approved.editors.add(self.user)
        assign_perm("change_company", self.user, self.not_approved)


class ModelTests(TestCase):
    def test_unicode(self):
        """The unicode representation of a company should contain its name."""
        company = models.Company(name="MyCompany")
        self.assertIn("MyCompany", str(company))

    def test_absolute_url(self):
        company = models.Company(name="MyCompany", pk=123)
        self.assertEqual("/companies/show/123/", company.get_absolute_url())


class DetailsViewTests(CompanyTestsMixin, TestCase):
    def test_approved_company(self):
        response = self.client.get("/companies/show/1/")
        self.assertEqual(response.status_code, 200)

    def test_not_approved_company(self):
        response = self.client.get("/companies/show/2/")
        self.assertEqual(response.status_code, 404)

    def test_not_approved_but_editor_visible(self):
        self.client.login(username="username", password="password")
        response = self.client.get("/companies/show/2/")
        self.assertEqual(response.status_code, 200)


class ListingTests(CompanyTestsMixin, TestCase):
    def test_listing_approved(self):
        """
        Only approved companies should be included in the listing view.
        """
        response = self.client.get("/companies/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["company_list"]), [self.approved])

    def test_listing_editor_logged_in(self):
        """
        If the editor of a not approved company is logged in, this company
        is included in the context.
        """
        self.client.login(username="username", password="password")
        response = self.client.get("/companies/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["unapproved_companies"]), [self.not_approved])


class CreationTests(TestCase):
    def setUp(self):
        # FIXME#40: Find out why the user already exists and clean up this code to simply create the test user.
        self.user = User.objects.filter(username="user").first()
        if self.user is None:
            self.user = User.objects.create_user(username="user", password="password", email="e@mail.com")

    def tearDown(self):
        self.user.delete()
        self.client.logout()

    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_create_logged_out(self):
        """
        If the user is logged out, creating a new company entry should be
        prohibited and redirect the user to the login form.
        """
        response = self.client.get("/companies/submit/")
        self.assertRedirects(response, "/accounts/signin/?next=/companies/submit/")

    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_create_logged_in(self):
        self.client.login(username="user", password="password")
        response = self.client.get("/companies/submit/")
        self.assertEqual(200, response.status_code)

        response = self.client.post(
            "/companies/submit/",
            {
                "name": "My Company",
                "website": "http://company.com",
                "address_line": "Street 123",
                "postal_code": "8010",
                "city": "Graz",
                "country": "AT",
            },
        )
        self.assertRedirects(response, "/companies/show/1/")


class UpdateViewTests(CompanyTestsMixin, TestCase):
    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_login_required(self):
        response = self.client.get("/companies/update/1/")
        self.assertRedirects(response, "/accounts/signin/?next=/companies/update/1/")

    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_404_on_not_existing_company(self):
        self.client.login(username="username", password="password")
        response = self.client.get("/companies/update/3/")
        self.assertEqual(response.status_code, 404)

    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_404_if_not_allowed(self):
        self.client.login(username="username", password="password")
        response = self.client.get("/companies/update/1/")
        self.assertEqual(response.status_code, 404)

    # FIXME#40: Remove initial "_" from test name and fix it.
    def _test_ok_if_editor(self):
        self.client.login(username="username", password="password")
        response = self.client.get("/companies/update/2/")
        self.assertEqual(response.status_code, 200)
