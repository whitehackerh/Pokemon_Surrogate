from rest_framework import serializers

class RemoveRequestValidator(serializers.Serializer):
    request_id = serializers.IntegerField()