from rest_framework import serializers
from django.core.validators import MinValueValidator

class RemoveListingValidator(serializers.Serializer):
    listing_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()