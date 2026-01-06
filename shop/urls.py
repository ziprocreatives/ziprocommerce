from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet

# 1. Initialize the router
router = DefaultRouter()

# 2. Register the ViewSet
# Leave the prefix empty ('') because you already have 'api/shop/' in config/urls.py
router.register(r'', ShopViewSet, basename='shop')

# 3. Include the router URLs
urlpatterns = [
    path('', include(router.urls)),
]