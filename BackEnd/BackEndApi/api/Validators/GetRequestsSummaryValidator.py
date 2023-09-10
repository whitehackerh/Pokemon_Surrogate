from rest_framework import serializers

class GetRequestsSummaryValidator(serializers.Serializer):
    status = serializers.IntegerField(allow_null=True)