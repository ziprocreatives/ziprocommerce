from django.db import models
from image.models import Image
from rest_framework import viewsets
from image.serializer import ImagesSerializer
class ImageViewSets(viewsets.ModelViewSet):
    queryset=Image.objects.all()
    serializer_class=ImagesSerializer
    lookup_field="shop_id"
