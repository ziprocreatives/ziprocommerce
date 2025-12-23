
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shops/',include('shops.urls')),
    path('api/users/', include('profiles.urls')),

]
