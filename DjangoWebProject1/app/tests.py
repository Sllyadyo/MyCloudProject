"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/Дошашняя страница')
        self.assertContains(response, 'Дошашняя страница', 1, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/Контактная информация')
        self.assertContains(response, 'Контактная информация', 3, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/О нас')
        self.assertContains(response, 'О нас', 3, 200)
