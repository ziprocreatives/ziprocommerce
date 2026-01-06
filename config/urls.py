from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Built-in Django Admin
    path('admin/', admin.site.urls),
    # Your Custom App APIs
    path('api/admin/', include('admin.urls')),
    path('api/shop/', include('shop.urls')),
    path('api/social/', include('social.urls')),
    path('api/products/', include('products.urls')),
    path('api/details/', include('details.urls')),
    path('api/image/', include('image.urls')),
    path('api/customers/', include('customers.urls')),
]