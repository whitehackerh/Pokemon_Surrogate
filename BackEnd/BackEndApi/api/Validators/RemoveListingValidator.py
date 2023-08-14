from rest_framework import serializers

class RemoveListingValidator(serializers.Serializer):
    listing_id = serializers.IntegerField()
    seller_id = serializers.IntegerField()