from rest_framework import serializers

class GetAcceptsSummaryValidator(serializers.Serializer):
    status = serializers.IntegerField()
    client = serializers.BooleanField()