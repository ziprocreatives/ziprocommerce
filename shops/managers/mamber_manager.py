import random
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta

class ShopMemberManager(models.Manager):

    # ==========================================
    # 1. PRE-REGISTRATION WORKFLOW (OTP APP)
    # ==========================================

    def start_pre_registration(self, identifier):
        """Initializes OTP process via the central OTP app."""
        from otp.models import PreeRegistration
        
        # Calling centralized logic from the OTP model instance
        otp_service = PreeRegistration()
        result, message = otp_service.generate_otp(identifier)
        
        if result:
            return message, "Verification code sent to email."
        return None, message

    @transaction.atomic
    def finalize_registration(self, data):
        """Verifies OTP via central app and triggers Shop creation."""
        from otp.models import PreeRegistration
        
        # 1. Verify using the centralized system
        otp_service = PreeRegistration()
        success, member_or_msg = otp_service.verify_otp(
            data.get('identifier'), 
            data.get('code')
        )
        
        if not success:
            return None, member_or_msg 

        # 2. OTP is valid, proceed to creation logic
        try:
            # We use the separate creation function defined below
            creator = self.create_shop_with_creator(data)
            
            # 3. Success cleanup: member_or_msg is the PreeRegistration instance
            member_or_msg.delete() 
            
            return creator, "Shop and Account created successfully."
        except Exception as e:
            # transaction.atomic rolls back database changes if an error occurs
            return None, f"Registration failed during creation: {str(e)}"

    # ==========================================
    # 2. CORE BUSINESS LOGIC (Independent)
    # ==========================================

    def create_shop_with_creator(self, data):
        """
        Independent creation logic. 
        Creates: Shop -> ShopMember (Creator) -> ShopDetails.
        """
        from shops.models import Shop
        ShopName=data.get('shop_name')
        identifier=data.get('identifier')
        while True:
            rand=random.randint(1000, 9999)
            generated_url=f"{ShopName.lower().replace(' ', '-')}-{rand}"
            if not Shop.objects.filter(url=generated_url).exists():
                break
        # A. Create the Shop
        shop = Shop.objects.create(
            name=ShopName,
            url=generated_url
        )

        # B. Create the Creator (Attached to the shop)
        creator = self.create(
            shop=shop,
            nickname=data.get('nickname'),
            identifier=data.get('identifier'),
            password=data.get('password'),
            role='creator',
            is_verified=True
        )

        # C. Populate ShopDetails
        if hasattr(shop, 'details'):
            if 'description' in data:
                shop.details.description = data.get('description')
            if 'category' in data:
                shop.details.category = data.get('category', 'General')
            shop.details.save()

        return creator

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
            role=role,
            is_verified=True
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
        """Removes a staff member. Prevents creator self-deletion."""
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, admin_id, required_role='creator')
        if not allowed: return False, msg

        if str(admin_id) == str(target_id):
            return False, "Security Error: You cannot delete yourself."

        deleted_count, _ = self.filter(shop_id=shop_id, id=target_id).delete()
        if deleted_count > 0:
            return True, "Staff member removed from shop."
        return False, "Member not found."

    # ==========================================
    # 4. ACCESS & ROLE MANAGEMENT
    # ==========================================

    @transaction.atomic
    def handover_access(self, shop_id, current_creator_id, new_creator_id):
        """Transfers Ownership: Promotes a Handler and demotes the old Creator."""
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, current_creator_id, required_role='creator')
        if not allowed: return False, msg

        old_owner = self.filter(id=current_creator_id, shop_id=shop_id).first()
        new_owner = self.filter(id=new_creator_id, shop_id=shop_id).first()

        if not new_owner: return False, "Target member not found."

        new_owner.role = 'creator'
        old_owner.role = 'handler'
        new_owner.save()
        old_owner.save()
        return True, f"Ownership transferred to {new_owner.nickname}."

    def update_role(self, shop_id, admin_id, target_id, new_role):
        """Updates a staff member's role."""
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, admin_id, required_role='creator')
        if not allowed: return msg

        member = self.filter(id=target_id, shop_id=shop_id).first()
        if member:
            member.role = new_role
            member.save()
            return f"Role changed to {new_role}."
        return "Member not found."

    # ==========================================
    # 5. GRANULAR UPDATES & UTILITIES
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

    def delete_otp(self, member_id):
        """Clears OTP fields for existing members."""
        member = self.filter(id=member_id).first()
        if member:
            member.otp = 0
            member.otp_expire = None
            member.save()
            return "OTP record cleared."
        return "Member not found."