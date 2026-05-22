from django.test import TestCase
from django.urls import reverse

class DiplomaSmokeTests(TestCase):
    def test_homepage(self):
        response=self.client.get('/')
        self.assertIn(response.status_code,[200,302])

    def test_catalog(self):
        response=self.client.get('/catalog/')
        self.assertIn(response.status_code,[200,302])
<<<<<<< HEAD
def test_product_detail(self):
    # Если есть хотя бы один товар
    from siteapp.models import Product
    if Product.objects.exists():
        product = Product.objects.first()
        response = self.client.get(product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

def test_about_page(self):
    response = self.client.get('/about/')
    self.assertEqual(response.status_code, 200)

def test_admin_login(self):
    response = self.client.post('/admin/login/', {
        'username': 'admin',
        'password': 'adminpass'
    })
    # После успешного входа Django делает редирект (302)
    self.assertIn(response.status_code, [200, 302])
=======

    def test_admin_login(self):
        response=self.client.get('/admin/')
        self.assertEqual(response.status_code,200)
>>>>>>> 89f7712a25099520718883959bfce88ec1f1cc26
