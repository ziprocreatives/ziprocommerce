import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from shop.models import Shop

class Admin(models.Model):  # Renamed for clarity
    ROLE_CHOICES = [('creator', 'Creator'), ('handler', 'Handler')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ManyToManyField('shop.Shop', related_name='members', blank=True)
    nickname = models.CharField(max_length=50)
    identifier = models.EmailField()  # Removed unique=True; enforced via unique_together
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, default='', validators=[RegexValidator(r'^\d{4,6}$', 'OTP must be 4-6 digits')])  # Changed to CharField with validation
    is_verified = models.BooleanField(default=False)
    otp_expire = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='handler')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin'
        verbose_name = 'Admin'
        pass
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nickname} ({self.role}) @ {self.shop.title}"

