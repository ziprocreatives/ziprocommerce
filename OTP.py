from datetime import timezone, timedelta
from random import random


def generate_otp(self):
    """Generates a random 6-digit code valid for 10 minutes."""
    self.otp_code = str(random.randint(100000, 999999))
    self.otp_expiry = timezone.now() + timedelta(minutes=10)
    self.save()
    return self.otp_code,self.otp_expiry


def verify_otp(self, code):
    """Checks if the code is correct and not expired."""
    if self.otp_code == code and timezone.now() < self.otp_expiry:
        self.is_verified = True
        self.otp_code = None  # Clear code after success
        self.save()
        return True
    return False