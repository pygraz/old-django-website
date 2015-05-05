from django.test import TestCase

from . import models


class ModelTests(TestCase):
    def test_unicode(self):
        """The unicode representation of a company should contain its name."""
        company = models.Company(name='MyCompany')
        self.assertTrue('MyCompany' in unicode(company))

    def test_absolute_url(self):
        company = models.Company(name='MyCompany', pk=123)
        self.assertEqual('/companies/show/123/', company.get_absolute_url())
