from rest_framework import serializers

class GetListingsPersonalSummaryValidator(serializers.Serializer):
    seller_id = serializers.IntegerField()
    status = serializers.IntegerField()