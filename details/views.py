from rest_framework import viewsets
from admin import serializers
from details.models import Details
from details.serializer import DetailsSerializer

class DetailsViewSets(viewsets.ModelViewSet):
    queryset = Details.objects.all()
    serializer_class = DetailsSerializer
    lookup_field = 'shop_id'