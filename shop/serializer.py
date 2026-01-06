from django.db import transaction
from rest_framework import serializers

# Import your serializers
# from details.serializer import DetailsSerializer
# from image.serializer import ImagesSerializer
# from social.serializers import SocialSerializer
# from image.serializer import ImagesSerializer
# from admin.serializers import AdminSerializer
from shop.models import Shop
class ShopSerializer(serializers.ModelSerializer):
    # details = DetailsSerializer(required=False)
    # Image = ImagesSerializer(required=False)
    # socials = SocialSerializer(required=False)
    # admin=AdminSerializer(required=True)
    class Meta:
        model = Shop
        fields = "__all__"