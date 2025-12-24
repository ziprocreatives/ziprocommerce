from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product


class ProductBaseAPI(APIView):
    """Base class providing a unified response structure."""

    def api_response(self, success, msg, data=None, status_code=None):
        if not success:
            return Response({"status": "error", "message": msg},
                            status=status_code or status.HTTP_403_FORBIDDEN)
        return Response({"status": "success", "message": msg, "data": data},
                        status=status_code or status.HTTP_200_OK)


# --- 1. CORE CRUD ---

class ProductCreateAPI(ProductBaseAPI):
    def post(self, request, shop_id):
        member_id = request.data.get('member_id')
        # Sanitizing: only pass valid model fields to the manager
        valid_fields = ['name', 'price', 'stock', 'category', 'description', 'sku']
        product_data = {k: v for k, v in request.data.items() if k in valid_fields}

        product, msg = Product.objects.add_product(shop_id, member_id, **product_data)
        if not product:
            return self.api_response(False, msg)

        return self.api_response(True, msg, {"id": product.id, "sku": product.sku}, status.HTTP_201_CREATED)


class ProductUpdateAPI(ProductBaseAPI):
    def post(self, request, product_id):
        shop_id = request.data.get('shop_id')
        member_id = request.data.get('member_id')

        # Filter updates to prevent unexpected keyword arguments
        valid_fields = ['name', 'price', 'category', 'description', 'stock', 'is_active']
        updates = {k: v for k, v in request.data.items() if k in valid_fields}

        success, msg = Product.objects.update_product(product_id, shop_id, member_id, **updates)
        return self.api_response(success, msg)


# --- 2. INVENTORY & PRICING ---

class ProductStockAPI(ProductBaseAPI):
    def post(self, request, product_id):
        shop_id = request.data.get('shop_id')
        member_id = request.data.get('member_id')
        amount = request.data.get('amount', 0)

        success, msg = Product.objects.adjust_stock(product_id, shop_id, member_id, int(amount))
        return self.api_response(success, msg)


class ProductDiscountAPI(ProductBaseAPI):
    def post(self, request, product_id):
        shop_id = request.data.get('shop_id')
        member_id = request.data.get('member_id')
        percentage = request.data.get('percentage')

        success, msg = Product.objects.apply_discount(product_id, shop_id, member_id, float(percentage))
        return self.api_response(success, msg)


# --- 3. MEDIA & STATUS ---

class ProductImageUpdateAPI(ProductBaseAPI):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, product_id):
        shop_id = request.data.get('shop_id')
        member_id = request.data.get('member_id')
        image = request.FILES.get('image')

        success, msg = Product.objects.update_product_image(product_id, shop_id, member_id, image)
        return self.api_response(success, msg)


class ProductActionAPI(ProductBaseAPI):
    """Handles toggle and delete actions."""

    def post(self, request, product_id, action):
        shop_id = request.data.get('shop_id')
        member_id = request.data.get('member_id')

        if action == 'toggle':
            success, msg = Product.objects.toggle_active_status(product_id, shop_id, member_id)
        elif action == 'delete':
            perm = request.data.get('permanent', False)
            success, msg = Product.objects.delete_product(product_id, shop_id, member_id, permanent=perm)
        else:
            return self.api_response(False, "Invalid action", status_code=400)
        return self.api_response(success, msg)


# --- 4. PUBLIC SEARCH ---

class StorefrontCatalogAPI(APIView):
    def get(self, request, shop_id):
        products = Product.objects.smart_search(
            shop_id=shop_id,
            query=request.query_params.get('q'),
            category=request.query_params.get('category'),
            min_p=request.query_params.get('min'),
            max_p=request.query_params.get('max'),
            is_admin=request.query_params.get('admin') == 'true'
        )
        data = products.values('id', 'name', 'price', 'stock', 'image', 'sku', 'category')
        return Response({"status": "success", "results": list(data)})