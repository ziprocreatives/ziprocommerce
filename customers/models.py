import uuid
import random
import string
from django.db import models
from django.db.models import Q
from django.contrib.auth.hashers import make_password, identify_hasher, check_password
from django.utils import timezone
from datetime import timedelta

from customers.customer_manager import CustomerManager


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='customers')
    identifier = models.CharField(max_length=20, unique=True, editable=False)

    # Login Credentials
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128)

    # Personal Info
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    # OTP Section
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp_expired = models.DateTimeField(blank=True, null=True)

    # Status & Loyalty
    is_active = models.BooleanField(default=True)
    tier = models.CharField(max_length=10, default='BRONZE')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomerManager()

    class Meta:
        db_table = 'customers'
        constraints = [
            models.UniqueConstraint(fields=['email', 'shop'], name='unique_email_per_shop'),
            models.UniqueConstraint(fields=['phone', 'shop'], name='unique_phone_per_shop'),
        ]

    def save(self, *args, **kwargs):
        # Generate internal identifier
        if not self.identifier:
            self.identifier = self.generate_unique_identifier()

        # Handle Password Hashing
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def generate_unique_identifier(self):
        prefix = "CUST"
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            val = f"{prefix}-{code}"
            if not Customer.objects.filter(identifier=val).exists():
                return val

    def generate_otp(self):
        code = ''.join(random.choices(string.digits, k=6))
        self.otp = code
        self.otp_expired = timezone.now() + timedelta(minutes=10)
        self.is_verified = False
        self.save()
        return code

    def check_otp(self, input_code):
        if not self.otp or self.otp != input_code:
            return False, "Invalid code."
        if timezone.now() > self.otp_expired:
            return False, "OTP expired."

        self.is_verified = True
        self.otp = None
        self.save()
        return True, "Verified successfully."

    def __str__(self):
        return f"{self.email or self.phone} ({self.shop.name})"