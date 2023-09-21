from rest_framework import serializers

class SetAcceptValidator(serializers.Serializer):
    request_id = serializers.IntegerField()
    