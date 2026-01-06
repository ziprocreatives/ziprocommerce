from django.urls import path, include
from rest_framework.routers import DefaultRouter
from details.views import DetailsViewSets

router = DefaultRouter()

# Fixed: base_name -> basename
router.register("", DetailsViewSets, basename="details")

urlpatterns = [
    path("", include(router.urls))
]