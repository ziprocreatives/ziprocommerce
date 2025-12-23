import uuid
import os
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from .shop_manager import ShopManager

# --- HELPER FUNCTIONS FOR DYNAMIC PATHS ---
def get_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    # Path: shop_logos/shop-slug/logo.jpg
    return f'shop_logos/{instance.slug}/logo.{ext}'

def get_cover_path(instance, filename):
    ext = filename.split('.')[-1]
    # Path: shop_covers/shop-slug/cover.jpg
    return f'shop_covers/{instance.slug}/cover.{ext}'

def get_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    # Path: shop_profiles/shop-slug/profile.jpg
    return f'shop_profiles/{instance.slug}/profile.{ext}'


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, default='other')

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_shop'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ShopMember',
        related_name='staff_at_shops'
    )

    # Updated upload_to to use the functions defined above
    logo = models.ImageField(upload_to=get_logo_path, null=True, blank=True)
    cover_photo = models.ImageField(upload_to=get_cover_path, null=True, blank=True)
    shop_profile_picture = models.ImageField(upload_to=get_profile_path, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ShopManager()

    class Meta:
        db_table = 'shops'

    # --- DYNAMIC URL PROPERTIES ---
    @property
    def logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return f"{settings.STATIC_URL}images/defaults/default-logo.png"

    @property
    def cover_url(self):
        if self.cover_photo and hasattr(self.cover_photo, 'url'):
            return self.cover_photo.url
        return f"{settings.STATIC_URL}images/defaults/default-cover.jpg"

    @property
    def profile_url(self):
        if self.shop_profile_picture and hasattr(self.shop_profile_picture, 'url'):
            return self.shop_profile_picture.url
        return f"{settings.STATIC_URL}images/defaults/default-profile.png"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ... (ShopMember class remains the same)
class ShopMember(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, default='handler')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shop_members'
        unique_together = ('profile', 'shop')