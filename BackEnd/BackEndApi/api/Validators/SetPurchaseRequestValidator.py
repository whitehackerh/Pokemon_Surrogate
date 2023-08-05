from rest_framework import serializers

class SetPurchaseRequestValidator(serializers.Serializer):
    listing_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()
    