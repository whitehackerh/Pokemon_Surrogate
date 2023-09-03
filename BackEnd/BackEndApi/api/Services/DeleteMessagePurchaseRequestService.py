from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.PurchaseRequestMessages import PurchaseRequestMessages
from django.utils import timezone

class DeleteMessagePurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchase_requests_model = PurchaseRequests()
            purchase_request_message_model = PurchaseRequestMessages()
            message_id = request.get('message_id')
            purchase_request_id = request.get('purchase_request_id')
            purchase_request = purchase_requests_model.getPurchaseRequestDetail(purchase_request_id)
            message = purchase_request_message_model.getMessage(message_id)
            if purchase_request.count() == 1 and ServiceUtils.isEnableSendMessagePurchaseRequest(purchase_request[0].status) and message.sender_id == int(request.get('sender_id')):
                message.deleted_at = timezone.now()
                message.save()
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
