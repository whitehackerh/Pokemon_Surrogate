import os
from django.conf import settings
from api.Enums.Messages import Messages
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Accepts import Accepts
from api.Models.AcceptMessages import AcceptMessages

class GetMessagesAcceptService(BaseService):
    def service(self, request):
        try:
            acceptsModel = Accepts()
            acceptMessagesModel = AcceptMessages()
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            displayed_latest_id = request.data.get('displayed_latest_id')
            accept = acceptsModel.getAcceptDetail(accept_id)
            records = None
            if accept.count() == 1 and (accept[0].client_id == user_id or accept[0].contractor_id == user_id):
                if displayed_latest_id:
                    records = acceptMessagesModel.getMessagesLatest(accept_id, displayed_latest_id)                    
                else:
                    records = acceptMessagesModel.getMessages(accept_id)
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