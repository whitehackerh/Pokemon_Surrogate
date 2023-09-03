from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Enums.ListingStatus import ListingStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.PurchaseRequestMessages import PurchaseRequestMessages
from api.Models.PurchaseRequests import PurchaseRequests

class SetReadMessagesPurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchaseRequestsModel = PurchaseRequests()
            purchaseRequestMessagesModel = PurchaseRequestMessages()
            purchase_request_id = request.get('purchase_request_id')
            user_id = int(request.get('user_id'))
            displayed_latest_id = request.get('displayed_latest_id')
            purchase_request = purchaseRequestsModel.getPurchaseRequestDetail(purchase_request_id)
            if purchase_request.count() == 1 and (purchase_request[0].seller_id == user_id or purchase_request[0].buyer_id == user_id) and displayed_latest_id:
                purchaseRequestMessagesModel.setReadMessages(purchase_request_id, user_id, displayed_latest_id)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)