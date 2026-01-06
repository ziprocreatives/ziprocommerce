import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class PreRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,default='')
    otp_expires_at = models.DateTimeField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    from pre_registration.model_manager import ModelManager 
    objects = ModelManager()

    def __str__(self):
        return self.identifier

    class Meta:
        db_table = "pre_registration"
        verbose_name = "Pre Registration"
        verbose_name_plural = "Pre Registrations"