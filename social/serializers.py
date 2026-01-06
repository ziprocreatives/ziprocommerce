from rest_framework import serializers
from social.models import Social


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = "__all__"
        read_only_fields = ("id","shop","created_at","updated_at")
