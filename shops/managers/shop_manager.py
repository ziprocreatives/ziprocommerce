from django.db import models, transaction
class ShopManager(models.Manager):

    # ==========================================
    # 1. CORE CREATION & DELETION
    # ==========================================

    @transaction.atomic
    def create_shop_with_owner(self, creator_nickname, creator_email, creator_password, shop_name, **extra_details):
        from shops.models import ShopMember

        # 1. Create the Shop (triggers Shop.save() to create Sub-tables)
        shop = self.create(
            name=shop_name,
            url=extra_details.get('url')
        )

        # 2. Create the Creator (Admin)
        creator = ShopMember.objects.create(
            shop=shop,
            nickname=creator_nickname,
            identifier=creator_email,
            password=creator_password,
            role='creator',
            is_verified = True
        )

        # 3. Update Detail fields if provided during creation
        if 'description' in extra_details:
            self.update_description(shop.id, creator.id, extra_details.get('description'))
        if 'category' in extra_details:
            self.update_category(shop.id, creator.id, extra_details.get('category'))

        return shop

    def delete_shop(self, shop_id, member_id):
        allowed, msg = self._verify_access(shop_id, member_id, required_role='creator')
        if not allowed: return msg

        self.filter(id=shop_id).delete()
        return "Shop and all related data deleted."

    # ==========================================
    # 2. SHOP CORE FIELD UPDATES (Name, URL, Status)
    # ==========================================

    def update_name(self, s_id, m_id, new_name):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        shop = self.get(id=s_id)
        shop.name = new_name
        shop.save()
        return "Shop name updated."

    def update_url(self, s_id, m_id, new_url):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        shop = self.get(id=s_id)
        shop.url = new_url
        shop.save()
        return "Shop URL updated."

    def toggle_active_status(self, s_id, m_id, status: bool):
        allowed, msg = self._verify_access(s_id, m_id, required_role='creator')
        if not allowed: return msg
        shop = self.get(id=s_id)
        shop.is_active = status
        shop.save()
        return f"Shop {'activated' if status else 'deactivated'}."

    # ==========================================
    # 3. SHOP DETAILS FIELD UPDATES & DELETES
    # ==========================================

    # DESCRIPTION
    def update_description(self, s_id, m_id, text):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        details = self.get(id=s_id).details
        details.description = text
        details.save()
        return "Description updated."

    def delete_description(self, s_id, m_id):
        return self.update_description(s_id, m_id, None)

    # CATEGORY
    def update_category(self, s_id, m_id, category):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        details = self.get(id=s_id).details
        details.category = category or "General"
        details.save()
        return "Category updated."

    def delete_category(self, s_id, m_id):
        return self.update_category(s_id, m_id, "General")

    # ADDRESS
    def update_address(self, s_id, m_id, address):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        details = self.get(id=s_id).details
        details.address = address
        details.save()
        return "Address updated."

    def delete_address(self, s_id, m_id):
        return self.update_address(s_id, m_id, None)

    # CONTACT EMAIL
    def update_contact_email(self, s_id, m_id, email):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        details = self.get(id=s_id).details
        details.contact_email = email
        details.save()
        return "Contact email updated."

    def delete_contact_email(self, s_id, m_id):
        return self.update_contact_email(s_id, m_id, None)

    # PHONE NUMBER
    def update_phone_number(self, s_id, m_id, phone):
        allowed, msg = self._verify_access(s_id, m_id)
        if not allowed: return msg
        details = self.get(id=s_id).details
        details.phone_number = phone
        details.save()
        return "Phone number updated."

    def delete_phone_number(self, s_id, m_id):
        return self.update_phone_number(s_id, m_id, None)

    # ==========================================
    # 4. SECURITY GUARD
    # ==========================================

    def _verify_access(self, shop_id, member_id, required_role=None):
        from shops.models import ShopMember
        member = ShopMember.objects.filter(id=member_id, shop_id=shop_id,is_verified=True).first()
        if not member:
            return False, "Access Denied."
        if not member.shop.is_active and required_role != 'creator':
            return False, "Shop Inactive."
        if required_role and member.role != required_role:
            return False, f"Requires {required_role} permission."
        return True, member

    def activate_or_deactive_shop(self, shop_id,status=False):
        from shops.models import Shop
        shop = Shop.objects.filter(id=shop_id).first()
        if not shop:
            return False, "Shop does not exist."
        shop.is_active = status
        shop.save()
        return f"Shop Actavatoin Status: {status}"

