from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default = 'default.jpg', upload_to = 'profile_pictures')
    address = models.TextField(max_length=500, blank=True)
    contact_no = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)
        img = Image.open(self.profile_picture.path)
        if(img.height > 300 or img.width>300):
            output_size = (300,300)
            img.thumbnail(output_size,Image.ANTIALIAS)
            img.save(self.profile_picture.path)