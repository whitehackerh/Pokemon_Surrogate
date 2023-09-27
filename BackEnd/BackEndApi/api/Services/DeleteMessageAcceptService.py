from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Models.Accepts import Accepts
from api.Models.AcceptMessages import AcceptMessages
from django.utils import timezone

class DeleteMessageAcceptService(BaseService):
    def service(self, request):
        try:
            acceptsModel = Accepts()
            acceptMessagesModel = AcceptMessages()
            message_id = request.data.get('message_id')
            accept_id = request.data.get('accept_id')
            accept = acceptsModel.getAcceptDetail(accept_id)
            message = acceptMessagesModel.getMessage(message_id)
            if accept.count() == 1 and ServiceUtils.isEnableSendMessageAccept(accept[0].status) and message.sender_id == ServiceUtils.getUserId(request):
                message.deleted_at = timezone.now()
                message.save()
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
