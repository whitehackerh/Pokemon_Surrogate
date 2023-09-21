from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from django.db.models import Subquery, OuterRef

class Accepts(models.Model):
    request_id = models.IntegerField()
    client_id = models.IntegerField()
    contractor_id = models.IntegerField()
    price = models.IntegerField(null=True)
    status = models.IntegerField()
    canceled_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'accepts'