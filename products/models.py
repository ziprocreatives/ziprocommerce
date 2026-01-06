import uuid
from django.db import models
from django.utils.text import slugify
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE,blank=True, null=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, null=True,blank=True)  # For product URL
    category = models.CharField(max_length=100, db_index=True,default="General")
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True,null=True,blank=True)
    # Media
    image = models.ImageField(upload_to='products/%Y/%m/', null=True, blank=True)

    # Financials & Inventory
    price = models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'product'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
        ]

    def save(self, *args, **kwargs):
        import secrets
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f"PROD-{secrets.token_hex(4).upper()}"
        super().save(*args, **kwargs)

    def get_product_url(self):
        if self.shop and self.slug:
            return f"/{self.shop.url}/products/{self.slug}/"
        return "#"

    def __str__(self):
        return f"{self.name} ({self.sku})"