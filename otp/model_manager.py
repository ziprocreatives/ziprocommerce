from datetime import timezone
import random
from django.db import models, transaction
from otp.models import PreeRegistration

class MoodelManager(models.Manager):
    def generate_otp(self, identifier):
        if self.filter(identifier=identifier).exists():
            return None

        otp_code = str(random.randint(10000, 999999))

        registration, created = PreeRegistration.objects.update_or_create(
            defaults={
                'identifier': identifier,
                'otp_code': otp_code,
                'created_at': timezone.now()
            }
        )
        return True

    @transaction.atomic
    def verify_otp(self, identifier, code):
        from otp.models import PreeRegistration
        pending = PreeRegistration.objects.filter(identifier=identifier).first()

        if not pending:
            return None, "No registration session found."
        
        if pending.expired_at < timezone.now():
            pending.delete()
            return None, "OTP expired. Please start over."

        if pending.otp_code != str(code):
            return None, "Invalid OTP code."
        
        pending.delete()

        return True, "Account created successfully."