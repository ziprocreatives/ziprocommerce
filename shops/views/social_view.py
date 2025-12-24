from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ShopSocial

class BaseSocialAPI(APIView):
    """Helper to standardize manager responses for social links."""
    def handle_result(self, result_msg):
        if "Denied" in result_msg or "not found" in result_msg:
            return Response({"error": result_msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": result_msg}, status=status.HTTP_200_OK)

# --- FACEBOOK ---
class UpdateFacebookAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        url = request.data.get('value')
        msg = ShopSocial.objects.update_facebook(shop_id, m_id, url)
        return self.handle_result(msg)

class DeleteFacebookAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopSocial.objects.delete_facebook(shop_id, m_id)
        return self.handle_result(msg)

# --- INSTAGRAM ---
class UpdateInstagramAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        url = request.data.get('value')
        msg = ShopSocial.objects.update_instagram(shop_id, m_id, url)
        return self.handle_result(msg)

class DeleteInstagramAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopSocial.objects.delete_instagram(shop_id, m_id)
        return self.handle_result(msg)

# --- TWITTER (X) ---
class UpdateTwitterAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        url = request.data.get('value')
        msg = ShopSocial.objects.update_twitter(shop_id, m_id, url)
        return self.handle_result(msg)

class DeleteTwitterAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopSocial.objects.delete_twitter(shop_id, m_id)
        return self.handle_result(msg)

# --- WEBSITE ---
class UpdateWebsiteAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        url = request.data.get('value')
        msg = ShopSocial.objects.update_website(shop_id, m_id, url)
        return self.handle_result(msg)

class DeleteWebsiteAPI(BaseSocialAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopSocial.objects.delete_website(shop_id, m_id)
        return self.handle_result(msg)