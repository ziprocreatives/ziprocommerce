from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from shops.models import ShopImages


# Base helper for image responses
class BaseBrandingAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Necessary for file uploads

    def handle_result(self, result_msg):
        if "Denied" in result_msg or "not found" in result_msg:
            return Response({"error": result_msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": result_msg}, status=status.HTTP_200_OK)


# --- LOGO ---
class UpdateLogoAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        file_obj = request.FILES.get('image')  # Frontend should send file as 'image'

        if not file_obj:
            return Response({"error": "No image file provided."}, status=400)

        msg = ShopImages.objects.update_logo(shop_id, m_id, file_obj)
        return self.handle_result(msg)


class DeleteLogoAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopImages.objects.delete_logo(shop_id, m_id)
        return self.handle_result(msg)


# --- COVER ---
class UpdateCoverAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        file_obj = request.FILES.get('image')

        if not file_obj:
            return Response({"error": "No image file provided."}, status=400)

        msg = ShopImages.objects.update_cover(shop_id, m_id, file_obj)
        return self.handle_result(msg)


class DeleteCoverAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopImages.objects.delete_cover(shop_id, m_id)
        return self.handle_result(msg)


# --- BANNER (Your manager calls this 'profile') ---
class UpdateBannerAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        file_obj = request.FILES.get('image')

        if not file_obj:
            return Response({"error": "No image file provided."}, status=400)

        msg = ShopImages.objects.update_profile(shop_id, m_id, file_obj)
        return self.handle_result(msg)


class DeleteBannerAPI(BaseBrandingAPI):
    def post(self, request, shop_id):
        m_id = request.data.get('member_id')
        msg = ShopImages.objects.delete_profile(shop_id, m_id)
        return self.handle_result(msg)