from image.models import Image
from rest_framework import serializers


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ("id","shop","created_at","updated_at")

