from rest_framework import serializers

class GetMessagesPurchaseRequestValidator(serializers.Serializer):
    purchase_request_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    displayed_latest_id = serializers.IntegerField(allow_null=True)