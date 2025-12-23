from django.urls import path
from .views import *

urlpatterns = [
    # Core
    path('', ShopListCreateAPI.as_view(), name='shop-list'),
    path('create/', ShopListCreateAPI.as_view(), name='shop-create'),
    path('<uuid:shop_id>/', ShopDetailAPI.as_view(), name='shop-detail'),

    # Grouped Branding APIs (Use PATCH to update, DELETE to remove)
    path('<uuid:shop_id>/logo/', ShopLogoAPI.as_view(), name='shop-logo'),
    path('<uuid:shop_id>/cover/', ShopCoverAPI.as_view(), name='shop-cover'),
    path('<uuid:shop_id>/profile-picture/', ShopProfilePictureAPI.as_view(), name='shop-profile-pic'),

    # Text Updates
    path('<uuid:shop_id>/update-name/', ShopNameUpdateAPI.as_view(), name='update-name'),

    # Management
    path('<uuid:shop_id>/members/', ShopMemberAPI.as_view(), name='shop-members'),
    path('<uuid:shop_id>/transfer/', ShopTransferAPI.as_view(), name='shop-transfer'),
]