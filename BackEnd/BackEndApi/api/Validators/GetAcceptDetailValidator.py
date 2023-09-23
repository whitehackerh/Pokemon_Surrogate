from rest_framework import serializers

class GetAcceptDetailValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()