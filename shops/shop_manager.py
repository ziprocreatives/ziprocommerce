from django.db import models, transaction

class ShopManager(models.Manager):
    # --- 1. ACCESS CHECKS ---
    def is_admin(self, shop_id, profile):
        """Strictly checks for Admin role."""
        from .models import ShopMember
        return ShopMember.objects.filter(shop_id=shop_id, profile=profile, role='admin').exists()

    def is_handler(self, shop_id, profile):
        """Strictly checks for Handler role."""
        from .models import ShopMember
        return ShopMember.objects.filter(shop_id=shop_id, profile=profile, role='handler').exists()

    def has_any_access(self, shop_id, profile):
        """Checks if user is either Admin or Handler."""
        from .models import ShopMember
        return ShopMember.objects.filter(shop_id=shop_id, profile=profile).exists()

    # --- 2. CORE OPERATIONS ---
    @transaction.atomic
    def create_shop_with_owner(self, profile, **shop_data):
        from .models import ShopMember
        shop = self.create(owner=profile, **shop_data)
        ShopMember.objects.create(profile=profile, shop=shop, role='admin')
        return shop

    def add_handler_access(self, shop_id, profile):
        from .models import ShopMember
        return ShopMember.objects.update_or_create(
            shop_id=shop_id, profile=profile, defaults={'role': 'handler'}
        )

    # --- 3. BRANDING: UPDATE & DELETE ---
    def update_logo(self, shop_id, image_file):
        shop = self.get(id=shop_id)
        if shop.logo: shop.logo.delete(save=False)
        shop.logo = image_file
        shop.save()
        return shop

    def update_cover_photo(self, shop_id, image_file):
        shop = self.get(id=shop_id)
        if shop.cover_photo: shop.cover_photo.delete(save=False)
        shop.cover_photo = image_file
        shop.save()
        return shop

    def update_shop_profile_picture(self, shop_id, image_file):
        shop = self.get(id=shop_id)
        if shop.shop_profile_picture: shop.shop_profile_picture.delete(save=False)
        shop.shop_profile_picture = image_file
        shop.save()
        return shop

    def delete_logo(self, shop_id): return self._perform_image_deletion(shop_id, 'logo')
    def delete_cover_photo(self, shop_id): return self._perform_image_deletion(shop_id, 'cover_photo')
    def delete_shop_profile_picture(self, shop_id): return self._perform_image_deletion(shop_id, 'shop_profile_picture')

    def _perform_image_deletion(self, shop_id, field_name):
        shop = self.get(id=shop_id)
        image_field = getattr(shop, field_name, None)
        if image_field and bool(image_field):
            image_field.delete(save=False)
            setattr(shop, field_name, None)
            shop.save()
        return shop