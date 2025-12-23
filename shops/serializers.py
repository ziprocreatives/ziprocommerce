from rest_framework import serializers
from .models import Shop, ShopMember
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()

class ShopMemberSerializer(serializers.ModelSerializer):
    """Shows details of users connected to the shop."""
    profile_email = serializers.ReadOnlyField(source='profile.email')
    profile_username = serializers.ReadOnlyField(source='profile.username')

    class Meta:
        model = ShopMember
        fields = [
            'profile',
            'profile_email',
            'profile_username',
            'role',
            'joined_at'
        ]

class ShopSerializer(serializers.ModelSerializer):
    """
    Full Shop Serializer with dynamic image URLs and specific Manager integration.
    """
    # Nested members data
    members_detail = ShopMemberSerializer(source='shopmember_set', many=True, read_only=True)

    # Human-readable version of the category choice (e.g., "Electronics" instead of "elec")
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    # DYNAMIC IMAGE URLS (Linked to Model @property methods)
    logo_url = serializers.ReadOnlyField()
    cover_url = serializers.ReadOnlyField()
    profile_url = serializers.ReadOnlyField()

    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'slug', 'category', 'category_display',
            'is_active', 'logo', 'cover_photo', 'shop_profile_picture',
            'logo_url', 'cover_url', 'profile_url',
            'members_detail', 'created_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at']

        # CRITICAL: Hide raw paths from JSON, keep for form-data uploads
        extra_kwargs = {
            'logo': {'write_only': True},
            'cover_photo': {'write_only': True},
            'shop_profile_picture': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Uses ShopManager to create the shop and link the owner atomically.
        """
        # Get profile from context (passed by View in ShopListCreateAPI)
        profile = self.context.get('profile')

        if not profile or profile.is_anonymous:
            # Fallback for testing environments
            profile = User.objects.first()
            if not profile:
                raise serializers.ValidationError({"error": "No users found in database."})

        try:
            # Calls ShopManager.create_shop_with_owner
            return Shop.objects.create_shop_with_owner(
                profile=profile,
                **validated_data
            )
        except IntegrityError:
            raise serializers.ValidationError({
                "error": "This user already owns a shop. Only one shop allowed per owner."
            })
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})