import random
import string
from django.db import models, transaction
from django.db.models import Q, F, Min, Max, Count
from django.utils.text import slugify


class ProductManager(models.Manager):

    # ==========================================
    # 1. CORE CRUD & SECURITY (Revision 1: Context Binding)
    # ==========================================

    def add_product(self, shop_id, member_id, **data):
        # This MUST be uncommented so Python knows what 'Shop' is
        from shops.models import Shop

        # 1. Verify access
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed:
            return None, msg

        # 2. Get the actual Shop instance (Defensive check)
        try:
            shop_instance = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return None, "Shop not found."

        # 3. Clean the data dictionary strictly
        data.pop('shop_id', None)
        data.pop('shop', None)
        data.pop('member_id', None)

        if not data.get('sku'):
            data['sku'] = self.generate_unique_sku()

        # 4. Use the instance
        return self.create(shop=shop_instance, **data), "Product created successfully."

    def update_product(self, product_id, shop_id, member_id, **updates):
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        if 'name' in updates and 'slug' not in updates:
            updates['slug'] = slugify(updates['name'])

        count = self.filter(id=product_id, shop_id=shop_id).update(**updates)
        return (True, "Update successful.") if count > 0 else (False, "Product not found.")

    # ==========================================
    # 2. STATUS & SOFT DELETE (Revision 2: Data Integrity)
    # ==========================================

    def toggle_active_status(self, product_id, shop_id, member_id):
        """Hides/Shows product from storefront without deleting it."""
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        product = self.filter(id=product_id, shop_id=shop_id).first()
        if not product: return False, "Product not found."

        product.is_active = not product.is_active
        product.save()
        status = "Active" if product.is_active else "Inactive"
        return True, f"Product is now {status}."

    def delete_product(self, product_id, shop_id, member_id, permanent=False):
        """Supports both Soft Delete (is_active=False) and Hard Delete."""
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        query = self.filter(id=product_id, shop_id=shop_id)
        if not query.exists(): return False, "Product not found."

        if permanent:
            query.delete()
            return True, "Product permanently removed."
        else:
            query.update(is_active=False)  # Soft delete/Archive
            return True, "Product archived (Soft deleted)."

    # ==========================================
    # 3. ADVANCED SEARCH (Revision 3: Faceted Search)
    # ==========================================

    def smart_search(self, shop_id, query=None, category=None, min_p=None, max_p=None, is_admin=False):
        queryset = self.filter(shop_id=shop_id)

        # Non-admins only see active products with stock
        if not is_admin:
            queryset = queryset.filter(is_active=True, stock__gt=0)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(sku__iexact=query) | Q(category__icontains=query)
            )

        if category: queryset = queryset.filter(category__iexact=category)
        if min_p:    queryset = queryset.filter(price__gte=min_p)
        if max_p:    queryset = queryset.filter(price__lte=max_p)

        return queryset.distinct().order_by('-created_at')

    # ==========================================
    # 4. INVENTORY & PRICE (Revision 4: Atomic Operations)
    # ==========================================

    def adjust_stock(self, product_id, shop_id, member_id, amount):
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        product = self.filter(id=product_id, shop_id=shop_id).first()
        if not product: return False, "Product not found."

        if amount < 0 and (product.stock + amount) < 0:
            return False, "Insufficient stock."

        self.filter(id=product_id, shop_id=shop_id).update(stock=F('stock') + amount)
        return True, "Stock updated."

    def apply_discount(self, product_id, shop_id, member_id, percentage):
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        product = self.filter(id=product_id, shop_id=shop_id).first()
        if not product: return False, "Product not found."

        # Keep original price in compare_at_price for strikethrough UI
        original = product.price
        product.compare_at_price = original
        product.price = original - (original * percentage / 100)
        product.save()
        return True, "Discount applied."

    # ==========================================
    # 5. MEDIA & UTILS (Revision 5: File & SKU Safety)
    # ==========================================

    def update_product_image(self, product_id, shop_id, member_id, image_file):
        from shops.models import Shop
        allowed, msg = Shop.objects._verify_access(shop_id, member_id)
        if not allowed: return False, msg

        product = self.filter(id=product_id, shop_id=shop_id).first()
        if not product: return False, "Product not found."

        product.image = image_file
        product.save()
        return True, "Image updated."

    def generate_unique_sku(self, prefix="PROD"):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            sku = f"{prefix}-{code}"
            if not self.filter(sku=sku).exists():
                return sku