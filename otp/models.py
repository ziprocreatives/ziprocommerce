import random
from django.db import models, transaction
from django.utils import timezone
from otp.models import PreeRegistration

class MoodelManager(models.Manager):

    # ==========================================
    # 1. GENERATE OTP (Step 1)
    # ==========================================
    def generate_otp(self, identifier, user_data=None):
        if self.filter(identifier=identifier).exists():
            return False, "This identifier is already registered."
        otp_code = str(random.randint(100000, 999999))
        registration, created = PreeRegistration.objects.update_or_create(
            identifier=identifier,
            defaults={
                'otp_code': otp_code,
                'is_verified': False,
                'expired_at': timezone.now() + timezone.timedelta(minutes=15)
            }
        )
        return True, otp_code.to_string()

    # ==========================================
    # 2. VERIFY & CREATE (Step 2)
    # ==========================================
    @transaction.atomic
    def verify_otp(self, identifier, code):
        """
        Verifies the OTP and moves data to the final model (Shop or Customer).
        """
        # 1. Find the pending record
        pending = PreeRegistration.objects.filter(identifier=identifier).first()

        if not pending:
            return None, "No registration session found."

        # 2. Check Expiration
        if pending.expired_at < timezone.now():
            pending.delete()
            return None, "OTP has expired."

        # 3. Check OTP Code
        if pending.otp_code != str(code):
            return None, "Invalid OTP code."

        # 4. Mark as verified in temp table (optional)
        pending.is_verified = True
        pending.save()

        # 5. Create the actual User/Shop/Customer
        # self.model refers to whatever model this manager is attached to.
        # We use data from the pending record to populate fields.
        new_instance = self.create(
            identifier=identifier,
            is_verified=True,
            # **pending.data # Unpack other fields if using JSONField
        )

        # 6. Delete temp record after success
        pending.delete()

        return new_instance, "Account verified and created."