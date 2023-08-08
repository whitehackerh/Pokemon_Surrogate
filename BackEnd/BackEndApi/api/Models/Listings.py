from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.ListingStatus import ListingStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Models.ListingPictures import ListingPictures
from api.Models.GameTitles import GameTitles
from api.Models.Fees import Fees
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

    def getListingsPersonalSellingRecordsCount(self, seller_id, status):
        try:
            return Listings.objects.filter(seller_id=seller_id, status=status).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getListingsPersonalSoldRemovedRecordsCount(self, seller_id, statuses):
        try:
            return Listings.objects.filter(seller_id=seller_id, status__in=statuses).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getListingsPersonalSelling(self, seller_id, status, offset, limit):
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
    
    def getListingsPersonalSoldRemoved(self, seller_id, statuses, offset, limit):
        try:
            from api.models import Users
            queryset = Listings.objects.filter(
                seller_id=seller_id,
                status__in=statuses
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
                ),
                fee_percentage=Subquery(
                    Fees.objects.filter(
                        id=OuterRef('fee_id')
                    ).values('percentage')[:1]
                )
            )
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def updateListing(self, request):
        try:
            listing = Listings.objects.get(id=request.data.get('listing_id'))
            listing.game_title_id = request.data.get('game_title_id')
            listing.category = request.data.get('category')
            listing.listing_title = request.data.get('listing_title')
            listing.description = request.data.get('description')
            listing.price_negotiation = request.data.get('price_negotiation')
            listing.price = request.data.get('price')
            listing.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def updateListingStatus(self, listing_id, status):
        try:
            listing = Listings.objects.get(id=listing_id)
            listing.status = status
            listing.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)

    def getListingsPublicRecordsCount(self):
        try:
            return Listings.objects.filter(status=ListingStatus.SELLING).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getListingsPublic(self, offset, limit):
        try:
            queryset = Listings.objects.filter(
                status = ListingStatus.SELLING
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
            ).order_by('-id')[offset:offset+limit]
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def removeListing(self, listing_id):
        try:
            listing = Listings.objects.get(id=listing_id)
            listing.status = ListingStatus.REMOVED
            listing.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)