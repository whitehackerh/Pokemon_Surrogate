from rest_framework import serializers

class SetReadMessagesAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()
    displayed_latest_id = serializers.IntegerField()