from django.db import models

class ShopImageManager(models.Manager):

    # ==========================================
    # 1. HELPER: ACCESS & RECORD RETRIEVAL
    # ==========================================
    def _get_branding_record(self, shop_id, member_id):
        """Internal helper to verify access and get the branding instance."""
        # Use the central security check in ShopManager
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed:
            return None, msg

        branding = self.filter(shop_id=shop_id).first()
        if not branding:
            return None, "Branding record not found."
        return branding, "Success"

    # ==========================================
    # 2. LOGO METHODS
    # ==========================================
    def update_logo(self, s_id, m_id, file_obj):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        # If a logo already exists, delete the old file first
        if obj.logo:
            obj.logo.delete(save=False)

        obj.logo = file_obj
        obj.save()
        return "Logo updated successfully."

    def delete_logo(self, s_id, m_id):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        if obj.logo:
            # Physically remove file from storage
            obj.logo.delete(save=True)
            return "Logo deleted from storage."
        return "Logo is already empty."

    # ==========================================
    # 3. COVER METHODS
    # ==========================================
    def update_cover(self, s_id, m_id, file_obj):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        if obj.cover:
            obj.cover.delete(save=False)

        obj.cover = file_obj
        obj.save()
        return "Cover image updated."

    def delete_cover(self, s_id, m_id):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        if obj.cover:
            obj.cover.delete(save=True)
            return "Cover image deleted."
        return "Cover is already empty."

    # ==========================================
    # 4. BANNER METHODS
    # ==========================================
    def update_profile(self, s_id, m_id, file_obj):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        if obj.banner:
            obj.banner.delete(save=False)

        obj.banner = file_obj
        obj.save()
        return "Banner updated."

    def delete_profile(self, s_id, m_id):
        obj, msg = self._get_branding_record(s_id, m_id)
        if not obj: return msg

        if obj.banner:
            obj.banner.delete(save=True)
            return "Banner deleted."
        return "Banner is already empty."