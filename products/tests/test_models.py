from products.models import Customer, Order, Product,OrderItem
from django.http import response
from django.test import TestCase,Client, client
from django.urls import reverse
from django.urls.base import resolve
from django.contrib.auth.models import AnonymousUser, User

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username = "test",password = "supersecretpass")
        self.product1 = Product.objects.create(
            name='product1',
            owner = self.test_user,
            price = 500,
        )
        self.order1 = Order.objects.create(customer=self.test_user.customer,transaction_id = 12000232001022)
        self.orderitem1 = OrderItem.objects.create(product = self.product1,order = self.order1,quantity = 2)
    
    def test_get_cart_total(self):
        self.assertEqual(self.order1.get_cart_total,1000)
    def test_get_cart_item(self):
        self.assertEqual(self.order1.get_cart_item,2)
    def test_get_cart_vat(self):
        self.assertEqual(self.order1.get_cart_vat,self.order1.get_cart_vat)

    
