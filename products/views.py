from rest_framework import viewsets, permissions, exceptions
from . import models, serializers

class ProductViewSets(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = serializers.ProductSerializer
    lookup_field = "id"

    def get_queryset(self):
        shop_id = self.kwargs.get('shop_id')
        if shop_id:
            return models.Product.objects.filter(shop_id=shop_id)
        return models.Product.objects.all()

    def check_permissions(self, request):
        """
        Custom check: If no shop_id is in the URL, only allow safe methods (GET).
        """
        super().check_permissions(request)
        
        shop_id = self.kwargs.get('shop_id')
        
        # If accessing the root /product/ and trying to POST/PUT/DELETE
        if not shop_id and request.method not in permissions.SAFE_METHODS:
            raise exceptions.PermissionDenied(
                "CRUD operations are only allowed through a specific shop URL."
            )

    def perform_create(self, serializer):
        shop_id = self.kwargs.get('shop_id')
        # This is extra insurance, though check_permissions should catch it
        if not shop_id:
            raise exceptions.ValidationError({"detail": "Shop ID is required to create a product."})
            
        serializer.save(shop_id=shop_id)