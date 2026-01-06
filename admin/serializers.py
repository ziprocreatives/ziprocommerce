from rest_framework import serializers

from shop.models import Shop
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False)
    nickname = serializers.CharField(required=False, allow_blank=True)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), 
        many=True,
        required=True
    )
    shop_id=serializers.CharField(read_only=True,required=False)
    class Meta:
        model = Admin
        # Fields to include in the API
        fields = ['id', 'identifier', 'otp', 'password', 'nickname', 'shop', 'created_at', 'updated_at','shop_id']
        
        # 'shop' must be read_only so .save() doesn't look for it in request.data
        read_only_fields = ("id", "created_at", "updated_at")
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate(self, data):
        identifier = data.get('identifier')
        otp= data.get('otp')
        return data       