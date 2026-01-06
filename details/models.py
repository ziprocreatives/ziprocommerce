import uuid
from django.db import models

class Details(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.OneToOneField('shop.Shop', on_delete=models.CASCADE, related_name='details')
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255,default='new Shop')

    class Meta:
        db_table = 'details'
        verbose_name = 'detail'
        indexes = [
            models.Index(fields=['category']),
        ]
