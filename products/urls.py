from django.urls import path
from . import views

urlpatterns = [
    # Catalog (Public)
    path('shop/<uuid:shop_id>/catalog/', views.StorefrontCatalogAPI.as_view()),

    # Management (Private/Authenticated)
    path('<uuid:shop_id>/create/', views.ProductCreateAPI.as_view()),
    path('<uuid:product_id>/update/', views.ProductUpdateAPI.as_view()),
    path('<uuid:product_id>/image/', views.ProductImageUpdateAPI.as_view()),
    path('<uuid:product_id>/stock/', views.ProductStockAPI.as_view()),
    path('<uuid:product_id>/discount/', views.ProductDiscountAPI.as_view()),
    path('<uuid:product_id>/action/<str:action>/', views.ProductActionAPI.as_view()),
]