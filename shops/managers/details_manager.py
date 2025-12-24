from django.db import models


class ShopDetailsManager(models.Manager):

    # ==========================================
    # 1. HELPER: ACCESS & RECORD RETRIEVAL
    # ==========================================
    def _get_details_record(self, shop_id, member_id):
        """Internal helper to verify access and get the details instance."""
        # Use your central security check
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed:
            return None, msg

        details = self.filter(shop_id=shop_id).first()
        if not details:
            return None, "Details record not found."
        return details, "Success"

    # ==========================================
    # 2. DESCRIPTION METHODS
    # ==========================================
    def update_description(self, s_id, m_id, text):
        obj, msg = self._get_details_record(s_id, m_id)
        if not obj: return msg
        obj.description = text
        obj.save()
        return "Description updated successfully."

    def delete_description(self, s_id, m_id):
        return self.update_description(s_id, m_id, None)

    # ==========================================
    # 3. ADDRESS METHODS
    # ==========================================
    def update_address(self, s_id, m_id, address):
        obj, msg = self._get_details_record(s_id, m_id)
        if not obj: return msg
        obj.address = address
        obj.save()
        return "Address updated."

    def delete_address(self, s_id, m_id):
        return self.update_address(s_id, m_id, None)

    # ==========================================
    # 4. CATEGORY METHODS
    # ==========================================
    def update_category(self, s_id, m_id, category_name):
        obj, msg = self._get_details_record(s_id, m_id)
        if not obj: return msg
        obj.category = category_name or "General"
        obj.save()
        return "Category updated."

    def delete_category(self, s_id, m_id):
        # Resets to default value instead of None
        return self.update_category(s_id, m_id, "General")

    # ==========================================
    # 5. CONTACT EMAIL METHODS
    # ==========================================
    def update_contact_email(self, s_id, m_id, email):
        obj, msg = self._get_details_record(s_id, m_id)
        if not obj: return msg
        obj.contact_email = email
        obj.save()
        return "Contact email updated."

    def delete_contact_email(self, s_id, m_id):
        return self.update_contact_email(s_id, m_id, None)

    # ==========================================
    # 6. PHONE NUMBER METHODS
    # ==========================================
    def update_phone_number(self, s_id, m_id, phone):
        obj, msg = self._get_details_record(s_id, m_id)
        if not obj: return msg
        obj.phone_number = phone
        obj.save()
        return "Phone number updated."

    def delete_phone_number(self, s_id, m_id):
        return self.update_phone_number(s_id, m_id, None)