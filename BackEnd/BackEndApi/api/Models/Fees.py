from django.db import models
from django.db.models import Q
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions

class Fees(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'fees'
    
    def getAvailableFee(self):
        try:
            return Fees.objects.filter(Q(end__isnull=True)).order_by('-id').first()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)