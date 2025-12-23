# accounts/managers.py
from django.contrib.auth.models import UserManager


class ProfileManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        # No normalization as requested
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        # We set defaults for a regular customer
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    # Note: We are NOT defining create_superuser here.
    # If someone tries to run 'createsuperuser' in the terminal, it will fail.