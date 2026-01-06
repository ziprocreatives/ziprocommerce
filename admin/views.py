from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404

# Local app imports
from .models import Admin
from .serializers import AdminSerializer

# Other app imports
from pre_registration.models import PreRegistration
from shop.models import Shop

class AdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Admins. 
    Supports 2-step registration: OTP generation and OTP verification.
    """
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        identifier = request.data.get('identifier')
        otp = request.data.get('otp')

        # 1. Basic Validation
        if not identifier:
            return Response({"error": "Identifier is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Check if Admin already exists
        if Admin.objects.filter(identifier=identifier).exists():
            return Response({"error": "This identifier is already registered."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. PHASE 1: OTP Generation
        # Triggered if identifier is provided but otp is missing
        if not otp:
            pre_reg = PreRegistration.objects.create_pre_registration(identifier=identifier)
            return Response({
                "message": "OTP generated successfully.",
                "identifier": identifier,
                "otp": pre_reg.otp  # Included for development; remove in production
            }, status=status.HTTP_200_OK)
        
        # 4. PHASE 2: OTP Verification and Admin Creation
        else:
            is_verified, pre_reg_instance, msg = PreRegistration.objects.verify_otp(identifier, otp)
            
            if not is_verified:
                return Response({"error": msg or "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    
                    # Save the admin without a shop link for now
                    serializer.save() 

                return Response({
                    "message": "Admin created successfully. Shop can be linked later.",
                    "user": serializer.data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=True, methods=['post'], url_path='link-shop')
    # def link_shop(self, request, id=None):
    #     """
    #     Custom action to link this Admin to a Shop later.
    #     URL: POST /api/admin/members/<id>/link-shop/
    #     """
    #     admin_user = self.get_object()
    #     shop_id = request.data.get('shop_id')
        
    #     if not shop_id:
    #         return Response({"error": "shop_id is required."}, status=status.HTTP_400_BAD_REQUEST)
            
    #     shop = get_object_or_404(Shop, id=shop_id)
        
    #     admin_user.shop = shop
    #     admin_user.save()
        
    #     return Response({
    #         "message": f"Admin successfully linked to {shop.name}.",
    #         "shop_id": shop.id
    #     }, status=status.HTTP_200_OK)