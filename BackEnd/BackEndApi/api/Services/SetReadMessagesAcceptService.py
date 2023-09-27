from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.AcceptMessages import AcceptMessages
from api.Models.Accepts import Accepts

class SetReadMessagesAcceptService(BaseService):
    def service(self, request):
        try:
            acceptsModel = Accepts()
            acceptMessagesModel = AcceptMessages()
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            displayed_latest_id = request.data.get('displayed_latest_id')
            accept = acceptsModel.getAcceptDetail(accept_id)
            if accept.count() == 1 and (accept[0].client_id == user_id or accept[0].contractor_id == user_id) and displayed_latest_id:
                acceptMessagesModel.setReadMessages(accept_id, user_id, displayed_latest_id)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)