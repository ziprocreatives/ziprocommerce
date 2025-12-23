from django.db import models, transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class ProfileManager(models.Manager):

    # --- RETRIEVAL METHODS ---
    def get_all_profiles(self):
        return self.all()

    def get_verified_profiles(self):
        return self.filter(is_verified=True)

    def get_profile(self, identifier):
        """Finds a profile by ID (PK), Email, or Phone."""
        if not identifier: return None
        try:
            return self.get(pk=identifier)
        except (ObjectDoesNotExist, ValidationError, ValueError):
            pass

        if "@" in str(identifier):
            return self.filter(email=identifier).first()
        return self.filter(phone_number=identifier).first()

    # --- ACCOUNT ACTIONS ---
    def create_profile(self, password, email=None, phone_number=None, **extra_fields):
        # REQUIRE EITHER PHONE OR EMAIL
        if not email and not phone_number:
            raise ValidationError("You must provide either an email or a phone number.")

        if not password:
            raise ValidationError("A password is required.")

        with transaction.atomic(using=self._db):
            profile = self.model(
                email=email,
                phone_number=phone_number,
                **extra_fields
            )
            profile.set_password(password)  # Securely hash the password
            profile.save(using=self._db)
            return profile

    def update_profile(self, identifier, **updates):
        profile = self.get_profile(identifier)
        if not profile:
            raise ObjectDoesNotExist(f"Profile '{identifier}' not found.")

        with transaction.atomic(using=self._db):
            for field, value in updates.items():
                if field == 'password':
                    profile.set_password(value)
                else:
                    setattr(profile, field, value)
            profile.save(using=self._db)
            return profile

    def delete_profile(self, identifier):
        profile = self.get_profile(identifier)
        if profile:
            profile.delete()
            return True
        return False