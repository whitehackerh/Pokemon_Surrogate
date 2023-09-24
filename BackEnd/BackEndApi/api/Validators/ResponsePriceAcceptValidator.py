from rest_framework import serializers

class ResponsePriceAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()
    response = serializers.BooleanField()