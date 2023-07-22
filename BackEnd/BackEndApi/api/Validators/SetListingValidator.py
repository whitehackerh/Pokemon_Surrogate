from rest_framework import serializers
from django.core.validators import MinValueValidator

class SetListingValidator(serializers.Serializer):
    listing_id = serializers.IntegerField(allow_null=True)
    seller_id = serializers.IntegerField()
    game_title_id = serializers.IntegerField()
    category = serializers.IntegerField()
    listing_title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price_negotiation = serializers.IntegerField()
    price = serializers.IntegerField(validators=[MinValueValidator(1)])