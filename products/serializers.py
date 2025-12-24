from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # UUID and timestamps should be read-only
    id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # Custom fields for frontend display
    savings = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'model',
            'price',
            'discount_price',  # Added to support your manager's apply_discount
            'description',
            'stock',
            'product_url',
            'is_available',
            'image',
            'savings',
            'updated_at',
            'created_at'
        ]

    def get_savings(self, obj):
        """Calculates the currency amount saved if on sale."""
        if obj.discount_price and obj.discount_price < obj.price:
            return float(obj.price - obj.discount_price)
        return 0.0

    def get_is_on_sale(self, obj):
        """Returns True if a valid discount price exists."""
        return obj.discount_price is not None and obj.discount_price < obj.price

    def validate_price(self, value):
        """Ensure price is never negative."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_stock(self, value):
        """Ensure stock is a realistic number."""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value