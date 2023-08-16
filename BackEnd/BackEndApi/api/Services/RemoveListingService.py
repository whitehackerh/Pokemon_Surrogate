from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.ListingStatus import ListingStatus
from api.Models.Listings import Listings

class RemoveListingService(BaseService):
    def service(self, request):
        try:
            listing_id = request.get('listing_id')
            if ServiceUtils.isEnableUpdateListing(listing_id, request.get('seller_id')):
                model = Listings()
                model.updateListingStatus(listing_id, ListingStatus.REMOVED)
            else:
                raise CustomExceptions('Not Available.', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
