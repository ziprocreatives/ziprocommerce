import uuid
from django.db import models


class Product(models.Model):
    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Direct Relationship to Shop UUID
    # shop = models.ForeignKey(
    #     'Shop',
    #     on_delete=models.CASCADE,
    #     related_name='products'
    # )

    # Basic Info
    name = models.CharField(max_length=255)
    model=models.CharField(max_length=255,blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    # Financials (Decimal is best for precision)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    product_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    # Media (Direct path for easy testing)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return f"{self.name} - Shop: {self.shop.id}"
        return f"{self.name}"