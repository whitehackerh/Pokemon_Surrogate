import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Listings import Listings
from api.Models.ListingPictures import ListingPictures
from api.Models.Fees import Fees
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.PurchaseRequestMessages import PurchaseRequestMessages
from api.Enums.Path import Path
from api.Enums.Read import Read
from api.Enums.ListingStatus import ListingStatus

class SendMessagePurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchase_request_id = request.data.get('purchase_request_id')
            sender_id = int(request.data.get('sender_id'))
            message = request.data.get('message')
            if message == '':
                message = None
            if self.__enableExecute(purchase_request_id, sender_id, message, request.FILES):
                messageParams = {
                    'purchase_request_id': purchase_request_id,
                    'sender_id': sender_id,
                    'message': message,
                    'read': Read.UNREAD
                }
                model = PurchaseRequestMessages(**messageParams)
                model.save()

                if 'picture' in request.FILES:
                    message_id = model.id
                    ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.PURCHASE_REQUEST_MESSAGE_PICTURE_DIR))
                    ## filename : {id}_uuid.png
                    filepath = os.path.join(Path.PURCHASE_REQUEST_MESSAGE_PICTURE_DIR, f'{message_id}_{uuid.uuid4().hex}.png')
                    model.setPicture(message_id, filepath)
                    with open(os.path.join(settings.MEDIA_ROOT, filepath), 'wb') as f:
                        for chunk in request.FILES.get('picture').chunks():
                            f.write(chunk)    
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def __enableExecute(self, purchase_request_id, sender_id, message, files):
        model = PurchaseRequests()
        purchase_request = model.getPurchaseRequestDetail(purchase_request_id)
        if purchase_request.count() != 1:
            return False
        if purchase_request[0].seller_id != sender_id and purchase_request[0].buyer_id != sender_id:
            return False
        if not ServiceUtils.isEnableSendMessagePurchaseRequest(purchase_request[0].status):
            return False
        if not message and not 'picture' in files:
            return False
        return True
        


   