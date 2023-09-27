from rest_framework import serializers

class DeleteMessageAcceptValidator(serializers.Serializer):
    message_id = serializers.IntegerField()
    accept_id = serializers.IntegerField()