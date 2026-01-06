import uuid
from django.db import models


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.OneToOneField('shop.Shop', on_delete=models.CASCADE, related_name='image')
    logo = models.ImageField(upload_to='shop/logos/', null=True, blank=True)
    cover = models.ImageField(upload_to='shop/covers/', null=True, blank=True)
    banner = models.ImageField(upload_to='shop/banners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'image'
        verbose_name = 'image'

