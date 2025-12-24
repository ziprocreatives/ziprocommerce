import uuid
import datetime
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Import the Managers
from shops.managers import (
    ShopManager,
    ShopMemberManager,
    ShopDetailsManager,
    ShopImageManager,
    ShopSocialManager
)


# ==========================================
# 1. CORE SHOP MODEL
# ==========================================

class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    url = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShopManager()

    class Meta:
        db_table = 'shops'
        verbose_name = 'Shop'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            # Atomic creation of related tables to ensure data integrity
            ShopImages.objects.get_or_create(shop=self)
            ShopSocial.objects.get_or_create(shop=self)
            ShopDetails.objects.get_or_create(shop=self)

    def __str__(self):
        return self.name


# ==========================================
# 2. STAFF MODEL
# ==========================================

class ShopMember(models.Model):
    ROLE_CHOICES = [('creator', 'Creator'), ('handler', 'Handler')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='staff_members')
    nickname = models.CharField(max_length=50)
    identifier = models.EmailField(unique=True)  # Used for login/OTP
    password = models.CharField(max_length=128)
    otp = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    otp_expire = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='handler')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShopMemberManager()

    class Meta:
        db_table = 'shop_members'
        verbose_name = 'Shop Member'
        unique_together = ('shop', 'identifier')
        indexes = [
            models.Index(fields=['identifier', 'shop']),  # Vital for _verify_access
        ]

    def save(self, *args, **kwargs):
        # Hash password only if it's plain text
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nickname} ({self.role}) @ {self.shop.name}"


# ==========================================
# 3. BRANDING MODEL
# ==========================================

class ShopImages(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='branding')
    logo = models.ImageField(upload_to='shops/logos/', null=True, blank=True)
    cover = models.ImageField(upload_to='shops/covers/', null=True, blank=True)
    banner = models.ImageField(upload_to='shops/banners/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShopImageManager()

    class Meta:
        db_table = 'shop_branding'
        verbose_name = 'Shop Images'


# ==========================================
# 4. DETAILS MODEL
# ==========================================

class ShopDetails(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='details')
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    contact_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShopDetailsManager()

    class Meta:
        db_table = 'shop_details'
        verbose_name = 'Shop Detail'
        indexes = [
            models.Index(fields=['category']),
        ]


# ==========================================
# 5. SOCIAL MODEL
# ==========================================

class ShopSocial(models.Model):
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='socials')
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShopSocialManager()

    class Meta:
        db_table = 'shop_socials'
        verbose_name = 'Shop Social'


# ==========================================
# 6. STAGING (PRE-REGISTRATION) MODEL
# ==========================================

class PreeRegistration(models.Model):
    identifier = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    data = models.JSONField(default=dict)  # Stores password/nickname/shop_name
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'preregistration'
        verbose_name = 'Pending Registration'
        indexes = [
            models.Index(fields=['created_at']),  # For cleanup cron jobs
            models.Index(fields=['identifier']),  # For verification lookups
        ]

    def is_expired(self):
        # OTP expires in 10 minutes
        return self.created_at < timezone.now() - datetime.timedelta(minutes=10)

    def __str__(self):
        return f"Pending: {self.identifier}"