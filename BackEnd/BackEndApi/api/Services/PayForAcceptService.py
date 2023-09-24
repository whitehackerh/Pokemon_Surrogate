from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Models.Accepts import Accepts

class PayForAcceptService(BaseService):
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            model = Accepts()
            record = model.getAcceptDetail(accept_id)
            if record.count() == 1 and ServiceUtils.isEnablePaymentAccept(record[0].status, user_id, record[0].client_id, record[0].contractor_id):
                model.updateStatus(accept_id, AcceptStatus.AWAITING_DELIVERY)
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
