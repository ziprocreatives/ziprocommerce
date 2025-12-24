from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This points to shop/urls.py
    path('api/shop/', include('shops.urls')),
    path('api/product/', include('products.urls')),
    path('api/customecr/', include('customecrs.urls')),
]
