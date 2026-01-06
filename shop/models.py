import uuid
from django.db import models
from details.models import Details
from image.models import Image
from social.models import Social 


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shop'
        verbose_name = 'Shop'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            Image.objects.get_or_create(shop=self)
            Social.objects.get_or_create(shop=self)
            Details.objects.get_or_create(shop=self)
            
    def __str__(self):
        return str(self.id)



# ==========================================
# 4. DETAILS MODEL
# ==========================================




