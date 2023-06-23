from rest_framework import serializers

class GetProfilePictureValidator(serializers.Serializer):
    id = serializers.IntegerField()