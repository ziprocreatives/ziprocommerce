from django.db import models
import random
from django.utils import timezone
from datetime import timedelta

class ModelManager(models.Manager):
    def create_pre_registration(self, identifier):
        from pre_registration.models import PreRegistration
        if PreRegistration.objects.filter(identifier=identifier).exists():
            return None, "Pre-registration with this identifier already exists."

        otp = str(random.randint(10000, 999999))
        registration = PreRegistration.objects.create(
            identifier=identifier,
            otp=otp,
            updated_at=timezone.now(),
            otp_expires_at=timezone.now() + timedelta(minutes=15)
            )
        return registration

    def verify_otp(self, identifier, otp):
        from pre_registration.models import PreRegistration
        pending = PreRegistration.objects.filter(identifier=identifier).first()

        if not pending:
            return False,None, "No registration session found."
        
        if pending.otp_expires_at < timezone.now():
            pending.delete()
            return None, None,"OTP expired. Please start over."

        if pending.otp != str(otp):
            return False,None, "Invalid OTP code."
        
        pending.delete()

        return True, pending, "OTP verified successfully."