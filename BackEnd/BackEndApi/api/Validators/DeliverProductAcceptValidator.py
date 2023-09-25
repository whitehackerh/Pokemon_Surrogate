from rest_framework import serializers

class DeliverProductAcceptValidator(serializers.Serializer):
    accept_id = serializers.IntegerField()