from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import ShopDetails

class BaseShopDetailAPI(APIView):
    """Common helper to handle string responses from the manager."""
    def handle_manager_result(self, result_msg):
        if "Denied" in result_msg or "not found" in result_msg:
            return Response({"error": result_msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": result_msg}, status=status.HTTP_200_OK)

# --- DESCRIPTION ---
class UpdateDescriptionAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        text = request.data.get('value')
        msg = ShopDetails.objects.update_description(shop_id, m_id, text)
        return self.handle_manager_result(msg)

class DeleteDescriptionAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopDetails.objects.delete_description(shop_id, m_id)
        return self.handle_manager_result(msg)

# --- ADDRESS ---
class UpdateAddressAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        addr = request.data.get('value')
        msg = ShopDetails.objects.update_address(shop_id, m_id, addr)
        return self.handle_manager_result(msg)

class DeleteAddressAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopDetails.objects.delete_address(shop_id, m_id)
        return self.handle_manager_result(msg)

# --- CATEGORY ---
class UpdateCategoryAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        cat = request.data.get('value')
        msg = ShopDetails.objects.update_category(shop_id, m_id, cat)
        return self.handle_manager_result(msg)

class DeleteCategoryAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopDetails.objects.delete_category(shop_id, m_id)
        return self.handle_manager_result(msg)

# --- CONTACT EMAIL ---
class UpdateContactEmailAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        email = request.data.get('value')
        msg = ShopDetails.objects.update_contact_email(shop_id, m_id, email)
        return self.handle_manager_result(msg)

class DeleteContactEmailAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopDetails.objects.delete_contact_email(shop_id, m_id)
        return self.handle_manager_result(msg)

# --- PHONE NUMBER ---
class UpdatePhoneNumberAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        phone = request.data.get('value')
        msg = ShopDetails.objects.update_phone_number(shop_id, m_id, phone)
        return self.handle_manager_result(msg)

class DeletePhoneNumberAPI(BaseShopDetailAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopDetails.objects.delete_phone_number(shop_id, m_id)
        return self.handle_manager_result(msg)