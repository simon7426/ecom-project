from products.models import Product
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from products.views import ProductListView,ProductDetailView,cart,checkout
from django.contrib.auth.models import AnonymousUser, User

class testUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProductListView)
    '''
    def test_detail_url_is_resolved(self):
        url = reverse('product-detail',kwargs={'pk':self.pk})
        print(resolve(url))
        self.assertEquals(resolve(url).func, ProductDetailView)
    '''
    def test_cart_url_is_resolved(self):
        url = reverse('cart')
        print(resolve(url))
        self.assertEquals(resolve(url).func, cart)
    
    def test_checkout_url_is_resolved(self):
        url = reverse('checkout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, checkout)
