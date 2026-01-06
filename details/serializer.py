from details.models import Details
from rest_framework import serializers


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        # shop_id=serializers.CharField(required=True)
        # admin_id=serializers.CharField(required=True)
        fields = "__all__"
        read_only_fields = ("id","shop","created_at","updated_at")
     