from django.db import models
from django.db.models import Q, F
from django.utils import timezone
from django.contrib.auth.hashers import check_password


class CustomerManager(models.Manager):

    # ==========================================
    # 1. IDENTITY & AUTHENTICATION
    # ==========================================

    def find_by_credential(self, shop_id, credential):
        """Finds a customer by either email or phone within a specific shop."""
        return self.filter(
            Q(shop_id=shop_id) & (Q(email=credential) | Q(phone=credential))
        ).first()

    def register(self, shop_id, password, email=None, phone=None, **extra_fields):
        """Handles shop-scoped registration with uniqueness checks."""
        if not email and not phone:
            return None, "Must provide either an email or a phone number."

        # Check for existing credentials in this specific shop
        existing = self.filter(Q(shop_id=shop_id) & (Q(email=email) | Q(phone=phone)))
        if email and existing.filter(email=email).exists():
            return None, "Email already registered in this shop."
        if phone and existing.filter(phone=phone).exists():
            return None, "Phone number already registered in this shop."

        customer = self.create(
            shop_id=shop_id,
            email=email,
            phone=phone,
            password=password,  # Model save() hashes this
            **extra_fields
        )
        return customer, "Account created successfully."

    def authenticate_customer(self, shop_id, credential, password):
        """Custom login check using either email or phone."""
        customer = self.find_by_credential(shop_id, credential)
        if customer and check_password(password, customer.password):
            if not customer.is_active:
                return None, "Account is deactivated."
            return customer, "Login successful."
        return None, "Invalid credentials."

    # ==========================================
    # 2. OTP & VERIFICATION
    # ==========================================

    def request_otp(self, shop_id, credential):
        """Generates OTP and returns delivery method (Email vs SMS)."""
        customer = self.find_by_credential(shop_id, credential)
        if not customer:
            return None, "Customer not found."

        otp_code = customer.generate_otp()

        # Determine routing
        method = "email" if (customer.email and credential == customer.email) else "sms"
        return customer, {"otp": otp_code, "method": method}

    def verify_otp(self, shop_id, credential, input_code):
        """Validates the code and consumes it."""
        customer = self.find_by_credential(shop_id, credential)
        if not customer:
            return False, "Customer not found."

        return customer.check_otp(input_code)

    # ==========================================
    # 3. SECURITY & PASSWORD MANAGEMENT
    # ==========================================

    def update_password(self, shop_id, identifier, current_password, new_password):
        """Standard password change (requires old password)."""
        customer = self.filter(shop_id=shop_id, identifier=identifier).first()
        if not customer:
            return False, "Customer not found."

        if not check_password(current_password, customer.password):
            return False, "Current password incorrect."

        customer.password = new_password  # save() hashes it
        customer.save()
        return True, "Password updated successfully."

    def reset_password_via_otp(self, shop_id, credential, otp_code, new_password):
        """Forgot password flow (requires valid OTP)."""
        customer = self.find_by_credential(shop_id, credential)
        if not customer:
            return False, "Customer not found."

        success, msg = customer.check_otp(otp_code)
        if success:
            customer.password = new_password
            customer.save()
            return True, "Password reset successful."
        return False, msg

    # ==========================================
    # 4. SEGMENTED PROFILE UPDATES
    # ==========================================

    def update_basic_info(self, shop_id, identifier, first_name=None, last_name=None):
        """Updates legal/display names."""
        count = self.filter(shop_id=shop_id, identifier=identifier).update(
            first_name=first_name,
            last_name=last_name
        )
        return (True, "Profile updated.") if count > 0 else (False, "Customer not found.")

    def update_contact_phone(self, shop_id, identifier, new_phone):
        """Updates phone with collision check."""
        if self.filter(shop_id=shop_id, phone=new_phone).exclude(identifier=identifier).exists():
            return False, "This phone number is already registered in this shop."

        count = self.filter(shop_id=shop_id, identifier=identifier).update(
            phone=new_phone,
            is_verified=False  # Reset verification status on contact change
        )
        return (True, "Phone updated. Please verify.") if count > 0 else (False, "Customer not found.")

    # ==========================================
    # 5. E-COMMERCE STATS & ADMIN
    # ==========================================

    def increment_spending(self, shop_id, identifier, amount):
        """Atomic update of total spent (use during checkout)."""
        count = self.filter(shop_id=shop_id, identifier=identifier).update(
            total_spent=F('total_spent') + amount
        )
        return (True, "Balance updated.") if count > 0 else (False, "Customer not found.")

    def set_account_status(self, shop_id, identifier, is_active):
        """Admin action to ban/activate account."""
        count = self.filter(shop_id=shop_id, identifier=identifier).update(is_active=is_active)
        return (True, "Status updated.") if count > 0 else (False, "Customer not found.")