from django.db import models


class ShopSocialManager(models.Manager):

    # ==========================================
    # 1. HELPER: ACCESS & RECORD RETRIEVAL
    # ==========================================
    def _get_social_record(self, shop_id, member_id):
        """Internal helper to verify access and get the social instance."""

        # Use your central security check
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed:
            return None, msg

        socials = self.filter(shop_id=shop_id).first()
        if not socials:
            return None, "Social records not found for this shop."
        return socials, "Success"

    # ==========================================
    # 2. FACEBOOK METHODS
    # ==========================================
    def update_facebook(self, s_id, m_id, url):
        obj, msg = self._get_social_record(s_id, m_id)
        if not obj: return msg
        obj.facebook = url
        obj.save()
        return "Facebook link updated."

    def delete_facebook(self, s_id, m_id):
        return self.update_facebook(s_id, m_id, None)

    # ==========================================
    # 3. INSTAGRAM METHODS
    # ==========================================
    def update_instagram(self, s_id, m_id, url):
        obj, msg = self._get_social_record(s_id, m_id)
        if not obj: return msg
        obj.instagram = url
        obj.save()
        return "Instagram link updated."

    def delete_instagram(self, s_id, m_id):
        return self.update_instagram(s_id, m_id, None)

    # ==========================================
    # 4. TWITTER (X) METHODS
    # ==========================================
    def update_twitter(self, s_id, m_id, url):
        obj, msg = self._get_social_record(s_id, m_id)
        if not obj: return msg
        obj.twitter = url
        obj.save()
        return "Twitter link updated."

    def delete_twitter(self, s_id, m_id):
        return self.update_twitter(s_id, m_id, None)

    # ==========================================
    # 5. WEBSITE METHODS
    # ==========================================
    def update_website(self, s_id, m_id, url):
        obj, msg = self._get_social_record(s_id, m_id)
        if not obj: return msg
        obj.website = url
        obj.save()
        return "Website URL updated."

    def delete_website(self, s_id, m_id):
        return self.update_website(s_id, m_id, None)