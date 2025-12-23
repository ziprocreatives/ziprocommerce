from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Shop
from .serializers import ShopSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# --- 1. LIST & CREATE ---
class ShopListCreateAPI(APIView):
    def get(self, request):
        search = request.query_params.get('search')
        status_f = request.query_params.get('status')
        if search:
            shops = Shop.objects.search_by_title(search)
        elif status_f == 'active':
            shops = Shop.objects.get_active_shops()
        elif status_f == 'deactivated':
            shops = Shop.objects.get_deactivated_shops()
        else:
            shops = Shop.objects.get_all_shops()
        return Response(ShopSerializer(shops, many=True).data)

    def post(self, request):
        user_id = request.data.get('user_id')
        profile = get_object_or_404(User, id=user_id) if user_id else request.user

        if profile.is_anonymous:
            profile = User.objects.first()

        serializer = ShopSerializer(data=request.data, context={'profile': profile})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 2. BRANDING & CORE UPDATES (ROLE: ADMIN ONLY) ---

class ShopLogoAPI(APIView):
    def patch(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('logo')
        if not file: return Response({"error": "No logo provided"}, status=400)
        shop = Shop.objects.update_logo(shop_id, file)
        return Response({"message": "Logo updated", "logo_url": shop.logo_url})

    def delete(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        Shop.objects.delete_logo(shop_id)
        return Response({"message": "Logo removed successfully"})


class ShopCoverAPI(APIView):
    def patch(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('cover_photo')
        if not file: return Response({"error": "No cover provided"}, status=400)
        shop = Shop.objects.update_cover_photo(shop_id, file)
        return Response({"message": "Cover updated", "cover_url": shop.cover_url})

    def delete(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        Shop.objects.delete_cover_photo(shop_id)
        return Response({"message": "Cover photo removed successfully"})


class ShopProfilePictureAPI(APIView):
    def patch(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('shop_profile_picture')
        if not file: return Response({"error": "No profile picture provided"}, status=400)
        shop = Shop.objects.update_shop_profile_picture(shop_id, file)
        return Response({"message": "Profile picture updated", "profile_url": shop.profile_url})

    def delete(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        Shop.objects.delete_shop_profile_picture(shop_id)
        return Response({"message": "Profile picture removed successfully"})


class ShopNameUpdateAPI(APIView):
    """Restricted to Admin only."""

    def patch(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Only Admins can change the shop name."}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        if not name: return Response({"error": "Name required"}, status=400)
        shop = get_object_or_404(Shop, id=shop_id)
        shop.name = name
        shop.save()
        return Response({"message": "Name updated", "new_name": shop.name, "slug": shop.slug})


# --- 3. VIEW & MEMBERSHIP ---

class ShopDetailAPI(APIView):
    def get(self, request, shop_id):
        # Admins and Handlers can both view details
        if not Shop.objects.has_any_access(shop_id, request.user):
            return Response({"error": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        shop = get_object_or_404(Shop, id=shop_id)
        return Response(ShopSerializer(shop).data)


class ShopMemberAPI(APIView):
    def post(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        p_id = request.data.get('profile_id')
        profile = get_object_or_404(User, id=p_id)
        Shop.objects.add_handler_access(shop_id, profile)
        return Response({"message": f"Access granted to {profile.username}"})


class ShopTransferAPI(APIView):
    def post(self, request, shop_id):
        if not Shop.objects.is_admin(shop_id, request.user):
            return Response({"error": "Admin privileges required."}, status=status.HTTP_403_FORBIDDEN)

        new_owner = get_object_or_404(User, id=request.data.get('new_owner_id'))
        Shop.objects.transfer_ownership(shop_id, new_owner)
        return Response({"message": "Ownership successfully transferred."})