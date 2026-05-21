from django.test import TestCase
from django.urls import reverse

class DiplomaSmokeTests(TestCase):
    def test_homepage(self):
        response=self.client.get('/')
        self.assertIn(response.status_code,[200,302])

    def test_catalog(self):
        response=self.client.get('/catalog/')
        self.assertIn(response.status_code,[200,302])

    def test_admin_login(self):
        response=self.client.get('/admin/')
        self.assertEqual(response.status_code,200)
