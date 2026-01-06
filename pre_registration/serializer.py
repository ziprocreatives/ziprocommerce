from rest_framework import serializers
from pre_registration.models import Pre_registration
class PreRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pre_registration
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_verified')