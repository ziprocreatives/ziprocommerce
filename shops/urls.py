from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # 1. PRE-REGISTRATION & ONBOARDING (NEW)
    # ==========================================
    # Step 1: Submit info & Request OTP
    path('register/start/', views.StartPreRegistrationAPI.as_view(), name='register-start'),
    # Step 2: Verify OTP & Create Shop/Account
    path('register/finalize/', views.FinalizeRegistrationAPI.as_view(), name='register-finalize'),

    # ==========================================
    # 2. CORE SHOP MANAGEMENT
    # ==========================================
    # Note: shop/create/ is now handled by register/finalize/
    path('shop/<uuid:shop_id>/delete/', views.DeleteShopAPI.as_view(), name='shop-delete'),
    path('shop/<uuid:shop_id>/update-name/', views.UpdateShopNameAPI.as_view(), name='shop-update-name'),
    path('shop/<uuid:shop_id>/update-url/', views.UpdateShopURLAPI.as_view(), name='shop-update-url'),
    path('shop/<uuid:shop_id>/toggle-status/', views.ToggleShopActiveAPI.as_view(), name='shop-toggle-status'),

    # ==========================================
    # 3. SHOP DETAILS (Address, Category, etc.)
    # ==========================================
    path('<uuid:shop_id>/description/update/', views.UpdateDescriptionAPI.as_view()),
    path('<uuid:shop_id>/description/delete/', views.DeleteDescriptionAPI.as_view()),
    path('<uuid:shop_id>/address/update/', views.UpdateAddressAPI.as_view()),
    path('<uuid:shop_id>/address/delete/', views.DeleteAddressAPI.as_view()),
    path('<uuid:shop_id>/category/update/', views.UpdateCategoryAPI.as_view()),
    path('<uuid:shop_id>/category/delete/', views.DeleteCategoryAPI.as_view()),
    path('<uuid:shop_id>/email/update/', views.UpdateContactEmailAPI.as_view()),
    path('<uuid:shop_id>/email/delete/', views.DeleteContactEmailAPI.as_view()),
    path('<uuid:shop_id>/phone/update/', views.UpdatePhoneNumberAPI.as_view()),
    path('<uuid:shop_id>/phone/delete/', views.DeletePhoneNumberAPI.as_view()),

    # ==========================================
    # 4. BRANDING (Images)
    # ==========================================
    path('shop/<uuid:shop_id>/branding/logo/update/', views.UpdateLogoAPI.as_view()),
    path('shop/<uuid:shop_id>/branding/logo/delete/', views.DeleteLogoAPI.as_view()),
    path('shop/<uuid:shop_id>/branding/cover/update/', views.UpdateCoverAPI.as_view()),
    path('shop/<uuid:shop_id>/branding/cover/delete/', views.DeleteCoverAPI.as_view()),
    path('shop/<uuid:shop_id>/branding/banner/update/', views.UpdateBannerAPI.as_view()),
    path('shop/<uuid:shop_id>/branding/banner/delete/', views.DeleteBannerAPI.as_view()),

    # ==========================================
    # 5. SOCIAL MEDIA LINKS
    # ==========================================
    path('<uuid:shop_id>/facebook/update/', views.UpdateFacebookAPI.as_view()),
    path('<uuid:shop_id>/facebook/delete/', views.DeleteFacebookAPI.as_view()),
    path('<uuid:shop_id>/instagram/update/', views.UpdateInstagramAPI.as_view()),
    path('<uuid:shop_id>/instagram/delete/', views.DeleteInstagramAPI.as_view()),
    path('<uuid:shop_id>/twitter/update/', views.UpdateTwitterAPI.as_view()),
    path('<uuid:shop_id>/twitter/delete/', views.DeleteTwitterAPI.as_view()),
    path('<uuid:shop_id>/website/update/', views.UpdateWebsiteAPI.as_view()),
    path('<uuid:shop_id>/website/delete/', views.DeleteWebsiteAPI.as_view()),

    # ==========================================
    # 6. MEMBERS, AUTH & STAFF
    # ==========================================
    # Auth & OTP (For existing members logging in)
    path('otp/generate/', views.GenerateOtpAPI.as_view()),
    path('otp/verify/', views.VerifyOtpAPI.as_view()),
    path('otp/delete/<uuid:member_id>/', views.DeleteOtpAPI.as_view()),

    # Staff Management
    path('<uuid:shop_id>/staff/add/', views.AddStaffAPI.as_view()),
    path('<uuid:shop_id>/staff/get/<uuid:target_id>/', views.GetStaffMemberAPI.as_view()),
    path('<uuid:shop_id>/staff/delete/<uuid:target_id>/', views.DeleteStaffAPI.as_view()),
    path('<uuid:shop_id>/staff/update-role/<uuid:target_id>/', views.UpdateMemberRoleAPI.as_view()),
    path('<uuid:shop_id>/staff/handover/', views.HandoverAccessAPI.as_view()),

    # Profile Updates
    path('update-nickname/<uuid:member_id>/', views.UpdateMemberNicknameAPI.as_view()),
    path('update-email/<uuid:member_id>/', views.UpdateMemberEmailAPI.as_view()),
    path('update-password/<uuid:member_id>/', views.UpdateMemberPasswordAPI.as_view()),
]