from products.models import Product
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from accounts.views import *
from django.contrib.auth.models import AnonymousUser, User

class testUrls(SimpleTestCase):

    def test_signup_is_resolved(self):
        url = reverse('signup')
        print(resolve(url))
        self.assertEquals(resolve(url).func, signup)
    
    def test_profile_is_resolved(self):
        url = reverse('profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile)
    
    def test_update_is_resolved(self):
        url = reverse('update')
        print(resolve(url))
        self.assertEquals(resolve(url).func, update)
    

    
