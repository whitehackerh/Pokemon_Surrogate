import os
from django.conf import settings
from api.Enums.Messages import Messages
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.PurchaseRequestMessages import PurchaseRequestMessages

class GetMessagesPurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchaseRequestsModel = PurchaseRequests()
            purchaseRequestMessagesModel = PurchaseRequestMessages()
            purchase_request_id = request.get('purchase_request_id')
            user_id = int(request.get('user_id'))
            displayed_latest_id = request.get('displayed_latest_id')
            purchase_request = purchaseRequestsModel.getPurchaseRequestDetail(purchase_request_id)
            records = None
            if purchase_request.count() == 1 and (purchase_request[0].seller_id == user_id or purchase_request[0].buyer_id == user_id):
                if displayed_latest_id:
                    records = purchaseRequestMessagesModel.getMessagesLatest(purchase_request_id, displayed_latest_id)                    
                else:
                    records = purchaseRequestMessagesModel.getMessages(purchase_request_id)
            else:
                raise CustomExceptions(Messages.INVALID_DATA, ResponseCodes.INVALID_DATA)
            data = self.__formatResponseData(records)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        data = {}
        data['messages'] = []
        for record in records:
            messages = {
                'id': record.id,
                'sender_id': record.sender_id,
                'message': record.message,
                'read': record.read,
                'created_at': record.created_at
            }
            if record.picture:
                messages['picture'] = ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.picture))
            data['messages'].append(messages)
        return data