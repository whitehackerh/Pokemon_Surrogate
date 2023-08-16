from django.db import transaction
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Enums.ListingStatus import ListingStatus
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.Listings import Listings

class CancelTransactionPurchaseRequestService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            purchase_request_id = request.get('purchase_request_id')
            user_id = int(request.get('user_id'))
            purchaseRequestModel = PurchaseRequests()
            record = purchaseRequestModel.getPurchaseRequestDetail(purchase_request_id)
            if record.count() == 1 and (user_id == record[0].seller_id or user_id == record[0].buyer_id) and ServiceUtils.isEnableCancelPurchaseRequest(record[0].status):
                purchaseRequestModel.updateStatus(purchase_request_id, PurchaseRequestStatus.CANCELLED)
                listingsModel = Listings()
                listingsModel.updateListingStatus(record[0].listing_id, ListingStatus.REMOVED)
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
