from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Enums.ListingStatus import ListingStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listings import Listings
from api.models import Users
from api.Models.PurchaseRequests import PurchaseRequests

class SetPurchaseRequestService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            listing_id = request.get('listing_id')
            buyer_id = int(request.get('buyer_id'))
            listingsModel = Listings()
            usersModel = Users()
            listing = listingsModel.getListingDetail(listing_id)
            if listing.count() == 1 and usersModel.getUserProfile(buyer_id).id == buyer_id and listing[0].seller_id != buyer_id and ServiceUtils.isEnableUpdateListing(listing_id, listing[0].seller_id):
                purchaseRequestsModel = PurchaseRequests(**{
                    'listing_id': listing[0].id,
                    'seller_id': listing[0].seller_id,
                    'buyer_id': buyer_id,
                    'price': listing[0].price,
                    'status': PurchaseRequestStatus.AWAITING_PAYMENT
                })
                purchaseRequestsModel.save()
                listingsModel.updateListingStatus(listing_id, ListingStatus.IN_PROGRESS)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)