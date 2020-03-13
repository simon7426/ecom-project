from django.db import models
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