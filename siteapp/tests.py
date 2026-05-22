from django.test import TestCase, Client
from django.contrib.auth.models import User
from siteapp.models import Category, Product

class DiplomaSmokeTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            category=self.category,
            is_active=True
        )
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_catalog_page(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)