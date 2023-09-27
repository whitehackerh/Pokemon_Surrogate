import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Accepts import Accepts
from api.Models.AcceptMessages import AcceptMessages
from api.Enums.Path import Path
from api.Enums.Read import Read

class SendMessageAcceptService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            sender_id = ServiceUtils.getUserId(request)
            message = request.data.get('message')
            if message == '':
                message = None
            if self.__enableExecute(accept_id, sender_id, message, request.FILES):
                messageParams = {
                    'accept_id': accept_id,
                    'sender_id': sender_id,
                    'message': message,
                    'read': Read.UNREAD
                }
                model = AcceptMessages(**messageParams)
                model.save()

                if 'picture' in request.FILES:
                    message_id = model.id
                    ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.ACCEPT_MESSAGE_PICTURE_DIR))
                    ## filename : {id}_uuid.png
                    filepath = os.path.join(Path.ACCEPT_MESSAGE_PICTURE_DIR, f'{message_id}_{uuid.uuid4().hex}.png')
                    model.setPicture(message_id, filepath)
                    with open(os.path.join(settings.MEDIA_ROOT, filepath), 'wb') as f:
                        for chunk in request.FILES.get('picture').chunks():
                            f.write(chunk)    
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def __enableExecute(self, accept_id, sender_id, message, files):
        model = Accepts()
        accept = model.getAcceptDetail(accept_id)
        if accept.count() != 1:
            return False
        if accept[0].client_id != sender_id and accept[0].contractor_id != sender_id:
            return False
        if not ServiceUtils.isEnableSendMessageAccept(accept[0].status):
            return False
        if not message and not 'picture' in files:
            return False
        return True
        


   