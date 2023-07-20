from rest_framework import serializers

class GetListingDetailValidator(serializers.Serializer):
    listing_id = serializers.IntegerField()
    user_id = serializers.IntegerField(allow_null=True)