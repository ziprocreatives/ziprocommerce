from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # List only the fields you want to show to the user
        fields = [
            'id',
            'email',
            'phone_number',
            'username',
            'address',
            'birth_date',
            'bio',
            'personal_avatar',
            'created_at'
        ]
        # These fields can be seen but NOT changed via the API
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        """Custom validation to ensure email is lowercase"""
        return value.lower()