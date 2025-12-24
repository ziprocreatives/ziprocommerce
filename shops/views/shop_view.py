from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shops.models import Shop

# Base helper for consistent responses
class BaseShopAPI(APIView):
    def handle_result(self, result_msg):
        # Manager returns a string message or an error string
        if "Denied" in result_msg or "Inactive" in result_msg:
            return Response({"error": result_msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": result_msg}, status=status.HTTP_200_OK)

# --- CORE LIFECYCLE ---

class CreateShopAPI(APIView):
    """Handles initial shop creation and owner setup."""
    def post(self, request):
        data = request.data
        try:
            shop = Shop.objects.create_shop_with_owner(
                creator_nickname=data.get('nickname'),
                creator_email=data.get('email'),
                creator_password=data.get('password'),
                shop_name=data.get('shop_name'),
                # Extra details passed as kwargs
                url=data.get('url'),
                description=data.get('description'),
                category=data.get('category')
            )
            return Response({
                "message": "Shop created successfully.",
                "shop_id": shop.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DeleteShopAPI(BaseShopAPI):
    """Requires 'creator' role to delete."""
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = Shop.objects.delete_shop(shop_id, m_id)
        return self.handle_result(msg)

# --- CORE FIELD UPDATES ---

class UpdateShopNameAPI(BaseShopAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        new_name = request.data.get('value')
        msg = Shop.objects.update_name(shop_id, m_id, new_name)
        return self.handle_result(msg)

class UpdateShopURLAPI(BaseShopAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        new_url = request.data.get('value')
        msg = Shop.objects.update_url(shop_id, m_id, new_url)
        return self.handle_result(msg)

class ToggleShopActiveAPI(BaseShopAPI):
    """Requires 'creator' role to toggle."""
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        # Expects a boolean in the 'value' field
        status_val = request.data.get('value', False)
        msg = Shop.objects.toggle_active_status(shop_id, m_id, status_val)
        return self.handle_result(msg)