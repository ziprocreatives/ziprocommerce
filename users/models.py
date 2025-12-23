from django.db import models
from ziprocommerce.users.user_manager import ProfileManager


# Create your models here.
class Profille(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField(max_length=11)
    username = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics')
    cover_pic = models.ImageField(upload_to='cover_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProfileManager()
    def __str__(self):
        return self.id