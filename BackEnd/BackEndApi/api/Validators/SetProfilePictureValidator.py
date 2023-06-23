from rest_framework import serializers

class SetProfilePictureValidator(serializers.Serializer):
    id = serializers.IntegerField()
    delete = serializers.BooleanField()