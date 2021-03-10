from products.models import Product
from django.http import response
from django.test import TestCase,Client, client
from django.urls import reverse
from django.urls.base import resolve
from django.contrib.auth.models import AnonymousUser, User
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.cart_url = reverse('cart')
        self.checkout_url = reverse('checkout')
        self.test_user = User.objects.create(username = "test",password = "supersecretpass")
        self.product1 = Product.objects.create(
            name='product1',
            owner = self.test_user,
            price = 500,
        )
        self.recommendation_url = reverse('recommend')
        #self.detail_url = reverse('product-detail',args=['product1'])
        

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'products/home.html')
    
    def test_cart_GET(self):
        response = self.client.get(self.cart_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'products/cart.html')
    
    def test_checkout_GET(self):
        response = self.client.get(self.checkout_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'products/checkout.html')
    
    def test_detail_GET(self):
        response = self.client.get(reverse('product-detail',kwargs={'pk':self.product1.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'products/product_detail.html')
    
    def test_recommendation_GET(self):
        response = self.client.get(self.recommendation_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'products/recommend.html')
    

    

    

    
