import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

# Create your models here.

@deconstructible
class GenerateProfileImagePath():
    
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return os.path.join(path, name)
    
user_profile_image_path = GenerateProfileImagePath()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    bio = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=user_profile_image_path, null=True, blank=True)


    def __str__(self, *args, **kwargs):
        return f"{self.user.username}'s Profile"  