from rest_framework import serializers

class GetUserProfileValidator(serializers.Serializer):
    id = serializers.IntegerField()
