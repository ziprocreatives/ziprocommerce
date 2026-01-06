from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Shop
from .serializer import ShopSerializer
# from admin.models import Admin 

class ShopViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    lookup_field = 'id'
    
    # def create(self, request, *args, **kwargs):
    #     # 1. Get the admin who is creating this shop
    #     admin_id = request.data.get('admin_id')
    #     if not admin_id:
    #         return Response({"error": "Admin identifier required"}, status=400)

    #     try:
    #         admin_user = Admin.objects.get(id=admin_id)
    #     except Admin.DoesNotExist:
    #         return Response({"error": "Admin not found"}, status=404)

    #     # 2. Create the Shop using your serializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     # This handles the Shop and nested Details creation
    #     new_shop = serializer.save()

    #     # 3. Link the Shop to the Admin (ManyToMany)
    #     admin_user.shop.add(new_shop) 

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)