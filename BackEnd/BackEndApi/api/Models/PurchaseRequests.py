from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from django.db.models import Subquery, OuterRef
from api.Models.ListingPictures import ListingPictures
from api.Models.Listings import Listings
from api.Models.GameTitles import GameTitles
from api.Models.Fees import Fees

class PurchaseRequests(models.Model):
    listing_id = models.IntegerField()
    seller_id = models.IntegerField()
    buyer_id = models.IntegerField()
    price = models.IntegerField()
    price_in_negotiation = models.IntegerField(null=True)
    status = models.IntegerField()
    canceled_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'purchase_requests'
    
    def getPurchaseRequestsRecordsCount(self, statuses, seller_id=None, buyer_id=None):
        try:
            queryset = PurchaseRequests.objects.all()
            queryset = queryset.filter(status__in=statuses)
            if seller_id is not None:
                queryset = queryset.filter(seller_id=seller_id)
            elif buyer_id is not None:
                queryset = queryset.filter(buyer_id=buyer_id)
            return queryset.count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def getPurchaseRequests(self, offset, limit, statuses, seller_id=None, buyer_id=None):
        try:
            from api.models import Users
            seller_user_subquery = Users.objects.filter(id=OuterRef('seller_id')).values('nickname')[:1]
            buyer_user_subquery = Users.objects.filter(id=OuterRef('buyer_id')).values('nickname')[:1]
            queryset = PurchaseRequests.objects.filter(
                status__in=statuses
            ).annotate(
                smallest_sort_no=Subquery(
                    ListingPictures.objects.filter(
                        listing_id=OuterRef('listing_id'),
                        deleted_at__isnull=True
                    ).order_by('sort_no').values('sort_no')[:1]
                ),
                path=Subquery(
                    ListingPictures.objects.filter(
                        listing_id=OuterRef('listing_id'),
                        sort_no=OuterRef('smallest_sort_no'),
                        deleted_at__isnull=True
                    ).values('path')[:1]
                ),
                listing_title=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('listing_title')[:1]
                ),
                game_title_id=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('game_title_id')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                seller_nickname=Subquery(seller_user_subquery),
                buyer_nickname=Subquery(buyer_user_subquery)
            )
            if seller_id is not None:
                queryset = queryset.filter(seller_id=seller_id)
            elif buyer_id is not None:
                queryset = queryset.filter(buyer_id=buyer_id)
            queryset = queryset.order_by('-id')[offset:offset+limit]
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getPurchaseRequestDetail(self, purchase_request_id):
        try:
            from api.models import Users
            seller_nickname_subquery = Users.objects.filter(id=OuterRef('seller_id')).values('nickname')[:1]
            seller_profile_picture_subquery = Users.objects.filter(id=OuterRef('seller_id')).values('profile_picture')[:1]
            buyer_nickname_subquery = Users.objects.filter(id=OuterRef('buyer_id')).values('nickname')[:1]
            buyer_profile_picture_subquery = Users.objects.filter(id=OuterRef('buyer_id')).values('profile_picture')[:1]
            queryset = PurchaseRequests.objects.filter(
                id = purchase_request_id
            ).annotate(
                game_title_id=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('game_title_id')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                category=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('category')[:1]
                ),
                listing_title=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('listing_title')[:1]
                ),
                description=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('description')[:1]
                ),
                price_negotiation=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('price_negotiation')[:1]
                ),
                fee_id=Subquery(
                    Listings.objects.filter(
                        id=OuterRef('listing_id')
                    ).values('fee_id')[:1]
                ),
                fee_percentage=Subquery(
                    Fees.objects.filter(
                        id=OuterRef('fee_id')
                    ).values('percentage')[:1]
                ),
                seller_nickname=Subquery(seller_nickname_subquery),
                seller_profile_picture=Subquery(seller_profile_picture_subquery),
                buyer_nickname=Subquery(buyer_nickname_subquery),
                buyer_profile_picture=Subquery(buyer_profile_picture_subquery)
            )
            return queryset.all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def requestChangePrice(self, id, price):
        try:
            purchase_request = PurchaseRequests.objects.get(id=id)
            purchase_request.price_in_negotiation = price
            purchase_request.status = PurchaseRequestStatus.PRICE_NEGOTIATION
            purchase_request.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)