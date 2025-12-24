import random
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta


class ShopMemberManager(models.Manager):

    # ==========================================
    # 1. PRE-REGISTRATION (STAGING) LOGIC
    # ==========================================

    def start_pre_registration(self, email, raw_data):
        """
        Step 1: Collect email and data, store in 'PreeRegistration' staging table.
        Uses update_or_create so a user can request a new OTP if they didn't get the first one.
        """
        from shops.models import PreeRegistration

        # 1. Check if email is already in the real ShopMember table
        if self.filter(identifier=email).exists():
            return None, "This email is already registered to a shop."

        otp_code = str(random.randint(100000, 999999))

        # 2. Store data in staging table
        registration, created = PreeRegistration.objects.update_or_create(
            identifier=email,
            defaults={
                'otp_code': otp_code,
                'data': raw_data,  # Contains nickname, password, shop_name, etc.
                'created_at': timezone.now()
            }
        )
        return otp_code, "Verification code sent to email."

    @transaction.atomic
    def finalize_registration(self, email, code):
        """
        Step 2: Verify OTP from staging table and move data to permanent tables.
        This creates the Shop and the Creator simultaneously.
        """
        from shops.models import PreeRegistration, Shop

        # 1. Find the staging record
        pending = PreeRegistration.objects.filter(identifier=email).first()

        if not pending:
            return None, "No registration session found."

        if pending.is_expired():
            pending.delete()
            return None, "OTP expired. Please start over."

        if pending.otp_code != str(code):
            return None, "Invalid OTP code."

        # 2. Extract verified data
        data = pending.data

        # 3. Create the Shop (triggers Shop.save() to create sub-tables)
        shop = Shop.objects.create(
            name=data.get('shop_name'),
            url=data.get('shop_url')
        )

        # 4. Create the Creator (Admin)
        creator = self.create(
            shop=shop,
            nickname=data.get('nickname'),
            identifier=email,
            password=data.get('password'),
            role='creator',
            is_verified=True
        )

        # 5. Optional: Map extra fields to ShopDetails
        if 'description' in data:
            shop.details.description = data.get('description')
        if 'category' in data:
            shop.details.category = data.get('category', 'General')
        shop.details.save()

        # 6. Cleanup the staging table
        pending.delete()

        return creator, "Shop and Account created successfully."

    # ==========================================
    # 2. AUTHENTICATION & SECURITY (OTP)
    # ==========================================

    def generate_otp(self, email):
        """Generates a 6-digit code and sets expiry for 5 minutes."""
        # Using 'identifier' to match your updated model
        member = self.filter(identifier=email).first()
        if not member:
            return None, "Email not found."

        otp_code = random.randint(100000, 999999)
        member.otp = otp_code
        member.otp_expire = timezone.now() + timedelta(minutes=5)
        member.save()
        return otp_code, "OTP generated successfully."

    def verify_otp(self, email, code):
        """Verifies code and clears it upon success to prevent reuse."""
        member = self.filter(identifier=email).first()
        if not member or member.otp == 0:
            return False, "No active OTP request found."

        if member.otp_expire < timezone.now():
            return False, "OTP has expired."

        if member.otp == int(code):
            member.otp = 0  # Clear OTP after successful use
            member.save()
            return True, member
        return False, "Invalid OTP code."

    # ==========================================
    # 3. STAFF MANAGEMENT (Add, Get, Delete)
    # ==========================================

    def add_staff(self, shop_id, admin_id, nickname, email, password, role='handler'):
        """Only Creators can add new staff members."""
        from shops.models import Shop

        allowed, msg = Shop.objects._verify_access(shop_id, admin_id, required_role='creator')
        if not allowed: return None, msg

        return self.create(
            shop_id=shop_id,
            nickname=nickname,
            identifier=email,
            password=password,
            role=role
        ), "Staff member added successfully."

    def get_staff_by_id(self, shop_id, requester_id, target_id):
        """Retrieves a single staff member within a specific shop context."""
        from shops.models import Shop

        allowed, msg = Shop.objects._verify_access(shop_id, requester_id)
        if not allowed: return None, msg

        member = self.filter(shop_id=shop_id, id=target_id).first()
        if not member: return None, "Staff member not found."
        return member, "Success"

    def delete_staff(self, shop_id, admin_id, target_id):
        """Permanently removes a staff member. Prevents creator self-deletion."""
        from shops.models import Shop

        allowed, msg = Shop.objects._verify_access(shop_id, admin_id, required_role='creator')
        if not allowed: return False, msg

        if str(admin_id) == str(target_id):
            return False, "Security Error: You cannot delete yourself. Handover ownership first."

        deleted_count, _ = self.filter(shop_id=shop_id, id=target_id).delete()
        if deleted_count > 0:
            return True, "Staff member removed from shop."
        return False, "Member not found."

    # ==========================================
    # 4. ACCESS HANDOVER (Transfer Ownership)
    # ==========================================

    @transaction.atomic
    def handover_access(self, shop_id, current_creator_id, new_creator_id):
        """Swaps roles: Promotes a Handler to Creator and demotes the old Creator."""
        from shops.models import Shop

        allowed, msg = Shop.objects._verify_access(shop_id, current_creator_id, required_role='creator')
        if not allowed: return False, msg

        old_owner = self.filter(id=current_creator_id, shop_id=shop_id).first()
        new_owner = self.filter(id=new_creator_id, shop_id=shop_id).first()

        if not new_owner:
            return False, "Target member for handover not found."

        new_owner.role = 'creator'
        old_owner.role = 'handler'

        new_owner.save()
        old_owner.save()
        return True, f"Ownership transferred to {new_owner.nickname}."

    # ==========================================
    # 5. GRANULAR UPDATES
    # ==========================================

    def update_nickname(self, member_id, new_nickname):
        member = self.filter(id=member_id).first()
        if not member: return "Member not found."
        member.nickname = new_nickname
        member.save()
        return "Nickname updated."

    def update_email(self, member_id, new_email):
        if self.filter(identifier=new_email).exists():
            return "Email is already taken."
        member = self.filter(id=member_id).first()
        if not member: return "Member not found."
        member.identifier = new_email
        member.save()
        return "Email updated."

    def update_password(self, member_id, new_password):
        member = self.filter(id=member_id).first()
        if not member: return "Member not found."
        member.password = new_password
        member.save()
        return "Password updated."

    def update_role(self, shop_id, admin_id, target_id, new_role):
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, admin_id, required_role='creator')
        if not allowed: return msg

        member = self.filter(id=target_id, shop_id=shop_id).first()
        if member:
            member.role = new_role
            member.save()
            return f"Role changed to {new_role}."
        return "Member not found."

    def delete_otp(self, member_id):
        member = self.filter(id=member_id).first()
        if member:
            member.otp = 0
            member.otp_expire = None
            member.save()
            return "OTP record cleared."
        return "Member not found."