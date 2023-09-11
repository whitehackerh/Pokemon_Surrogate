from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from django.utils import timezone

class RequestPictures(models.Model):
    request_id = models.IntegerField()
    client_id = models.IntegerField()
    path = models.CharField(max_length=255)
    sort_no = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'request_pictures'

    def getRequestPictures(self, request_id):
        try:
            return RequestPictures.objects.filter(request_id=request_id, deleted_at__isnull=True).order_by('sort_no')
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)