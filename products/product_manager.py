from django.db import models
from django.db import transaction

class ProductManager(models.Manager):

    # --- RETRIEVAL FUNCTIONS ---

    def get_all_products(self):
        """Returns all products in the database."""
        return self.all()

    def get_activate_products(self):
        """Returns only products where is_available is True."""
        return self.filter(is_available=True)

    def get_deactivate_products(self):
        """Returns only products where is_available is False."""
        return self.filter(is_available=False)

    def get_product_by_id(self, product_id):
        """Returns a single product by UUID or None if not found."""
        return self.filter(id=product_id).first()

    def get_product_by_name(self, name):
        """Returns a queryset of products matching the name (case-insensitive)."""
        return self.filter(name__icontains=name)

    def get_product_by_price(self, min_price=None, max_price=None):
        """Filters products within a specific price range."""
        queryset = self.all()
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    # --- ACTION FUNCTIONS ---

    def create_product(self, shop, name, price, stock, **extra_fields):
        return self.create(
            shop=shop,
            name=name,
            price=price,
            stock=stock,
            **extra_fields
        )

    def update_product(self, product_id, **updates):
        return self.filter(id=product_id).update(**updates)

    def deactivate_product(self, product_id):
        return self.filter(id=product_id).update(is_available=False)

    def active_product(self, product_id):
        return self.filter(id=product_id).update(is_available=True)

    def increase_quantity(self, product_id, amount):
        product = self.get_product_by_id(product_id)
        if product:
            product.stock += amount
            product.save()
            return product.stock
        return None

    def decrease_quantity(self, product_id, amount):
        product = self.get_product_by_id(product_id)
        if product:
            if product.stock >= amount:
                product.stock -= amount
                product.save()
                return product.stock, "Success"
            return False, "Insufficient stock"
        return False, "Product not found"

    def apply_discount(self, product_id, discount_price):
        product = self.get_product_by_id(product_id)
        if product:
            product.discount_price = discount_price
            product.save()
            return product
        return None