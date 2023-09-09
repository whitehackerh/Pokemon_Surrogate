from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Models.GameTitles import GameTitles
from api.Models.Fees import Fees
from api.Models.Listings import Listings
from api.Models.ListingPictures import ListingPictures
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.Requests import Requests
from api.Models.RequestPictures import RequestPictures

__all__ = [
    'Users',
    'GameTitles',
    'Fees',
    'Listings',
    'ListingPictures',
    'PurchaseRequests',
    'PurchaseRequestMessages',
    'Requests',
    'RequestPictures'
]

class Users(AbstractUser):
    nickname = models.CharField(max_length=255)
    bank_account = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def getUserProfile(self, id):
        try:
            return Users.objects.get(id=id)
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def setUserProfile(self, request):
        try:
            user = Users.objects.get(id=request.get('id'))
            user.username = request.get('username')
            user.first_name = request.get('first_name')
            user.last_name = request.get('last_name')
            user.email = request.get('email')
            user.nickname = request.get('nickname')
            user.bank_account = request.get('bank_account')
            user.updated_at = timezone.now()
            user.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def setProfilePicture(self, id, path):
        try:
            user = Users.objects.get(id=id)
            user.profile_picture = path
            user.updated_at = timezone.now()
            user.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)