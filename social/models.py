import uuid
from django.db import models

# Create your models here.
class Social(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.OneToOneField('shop.Shop', on_delete=models.CASCADE, related_name='socials')
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.URLField(blank=True, null=True)
    phone=models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'shop_socials'
        verbose_name = 'Shop Social'
