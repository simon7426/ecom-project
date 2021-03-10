from accounts.models import Profile
from django.http import response
from django.test import TestCase,Client, client
from django.urls import reverse
from django.urls.base import resolve
from django.contrib.auth.models import AnonymousUser, User
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('profile')
        self.update_url = reverse('update')
        self.signup_url = reverse('signup')
        self.test_user = User.objects.create(username = "test",password = "supersecretpass")

    def test_profile_GET(self):
        self.client.login(username = "test",password = "supersecretpass")
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 302)
        #self.assertTemplateUsed(response,'accounts/profile.html')
    
    def test_signup_GET(self):
        #self.client.login(username = "test",password = "supersecretpass")
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'accounts/signup.html')
    
    def test_update_GET(self):
        self.client.login(username = "test",password = "supersecretpass")
        response = self.client.get(self.update_url)
        self.assertEquals(response.status_code, 302)
        #self.assertTemplateUsed(response,'accounts/update.html')
    