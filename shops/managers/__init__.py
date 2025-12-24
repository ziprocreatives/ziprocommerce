# managers/__init__.py

from .shop_manager import ShopManager
from .mamber_manager import (ShopMemberManager)
from .details_manager import ShopDetailsManager
from .image_manager import ShopImageManager
from .social_manager import ShopSocialManager

# This list defines what is public when someone imports from this folder
__all__ = [
    'ShopManager',
    'ShopMemberManager',
    'ShopDetailsManager',
    'ShopImageManager',
    'ShopSocialManager',
]