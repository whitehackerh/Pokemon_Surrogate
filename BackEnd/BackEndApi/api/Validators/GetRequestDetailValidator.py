from rest_framework import serializers

class GetRequestDetailValidator(serializers.Serializer):
    request_id = serializers.IntegerField()