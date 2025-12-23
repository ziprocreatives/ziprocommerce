from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .profile_manager import ProfileManager


class Profile(AbstractBaseUser, PermissionsMixin):
    # --- PRIMARY KEY ---
    id = models.BigAutoField(primary_key=True)

    # --- IDENTITY & AUTH ---
    email = models.EmailField(unique=True, blank=True, null=True, db_index=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, db_index=True)
    password = models.CharField(max_length=255)

    # --- PROFILE FIELDS ---
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    personal_avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    # --- OTP & VERIFICATION ---
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # --- PERMISSIONS & STATUS ---
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # --- TIMESTAMPS ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    # Django Auth Settings
    USERNAME_FIELD = 'email'  # Change to 'phone_number' if preferred
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def clean(self):
        """Final check to ensure either email or phone is present."""
        super().clean()
        if not self.email and not self.phone_number:
            raise ValidationError("You must provide either an email or a phone number.")

    def save(self, *args, **kwargs):
        """Force validation before saving to DB."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} | {self.email or self.phone_number}"