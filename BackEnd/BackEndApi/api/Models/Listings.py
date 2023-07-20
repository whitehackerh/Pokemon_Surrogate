from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Models.ListingPictures import ListingPictures
from api.Models.GameTitles import GameTitles
from django.db.models import Subquery, OuterRef

class Listings(models.Model):
    seller_id = models.IntegerField()
    game_title_id = models.IntegerField()
    category = models.IntegerField()
    listing_title = models.CharField(max_length=255)
    description = models.TextField()
    price_negotiation = models.IntegerField()
    price = models.IntegerField()
    fee_id = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'listings'

    def getListingsPersonalRecordsCount(self, seller_id, status):
        try:
            return Listings.objects.filter(seller_id=seller_id, status=status).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getListingsPersonal(self, seller_id, status, offset, limit):
        try:
            from api.models import Users
            queryset = Listings.objects.filter(
                seller_id=seller_id,
                status = status
            ).annotate(
                smallest_sort_no=Subquery(
                    ListingPictures.objects.filter(
                        listing_id=OuterRef('id'),
                        deleted_at__isnull=True
                    ).order_by('sort_no').values('sort_no')[:1]
                ),
                path=Subquery(
                    ListingPictures.objects.filter(
                        listing_id=OuterRef('id'),
                        sort_no=OuterRef('smallest_sort_no'),
                        deleted_at__isnull=True
                    ).values('path')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                nickname=Subquery(
                    Users.objects.filter(
                        id=seller_id
                    ).values('nickname')[:1]
                )
            ).order_by('-id')[offset:offset+limit]
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getListingDetail(self, listing_id):
        try:
            from api.models import Users
            queryset = Listings.objects.filter(
                id = listing_id
            ).annotate(
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                nickname=Subquery(
                    Users.objects.filter(
                        id=OuterRef('seller_id')
                    ).values('nickname')[:1]
                ),
                sellers_profile_picture=Subquery(
                    Users.objects.filter(
                        id=OuterRef('seller_id')
                    ).values('profile_picture')[:1]
                )
            )
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)