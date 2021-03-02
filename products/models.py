from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    image = models.ImageField(default = 'no_image.jpg', upload_to = 'product_pictures')
    date_posted = models.DateTimeField(default = timezone.now)
    price = models.DecimalField(max_digits = 8,decimal_places = 2)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    tags = TaggableManager()
    def save(self,*args,**kwargs):
        super(Product,self).save(*args,**kwargs)
        img = Image.open(self.image.path)
        if(img.height > 300 or img.width>300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk':self.pk})

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    Customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    district = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=10,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address




