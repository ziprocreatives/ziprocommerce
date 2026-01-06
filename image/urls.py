from django.urls import path, include
from rest_framework.routers import DefaultRouter

from image.views import ImageViewSets
router=DefaultRouter()
router.register('',ImageViewSets,basename="image")
urlpatterns = [
    path('', include(router.urls)),
]