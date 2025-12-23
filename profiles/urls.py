from django.urls import path
from .views import RegisterUser, UpdateUser, DeleteUser, AllUser

urlpatterns = [
    # Separate endpoints for each action
    path('register/', RegisterUser.as_view(), name='user-register'),
    path('update/', UpdateUser.as_view(), name='user-update'),
    path('delete/', DeleteUser.as_view(), name='user-delete'),

    # Keep your list view for admin or general lookups
    path('list/', AllUser.as_view(), name='user-list'),
]