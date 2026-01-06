from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminViewSet

router = DefaultRouter()
router.register(r'members', AdminViewSet, basename='admin-member')

# 3. Define urlpatterns
urlpatterns = [
    # This includes all the routes registered above
    path('', include(router.urls)),
]