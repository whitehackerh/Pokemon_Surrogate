from rest_framework import serializers

class GetMessagesAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()
    displayed_latest_id = serializers.IntegerField(allow_null=True)