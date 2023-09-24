from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Models.Accepts import Accepts

class RequestPriceAcceptService(BaseService):
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            request_price = request.data.get('request_price')
            user_id = ServiceUtils.getUserId(request)
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            model = Accepts()
            record = model.getAcceptDetail(accept_id)
            if record.count() == 1 and ServiceUtils.isEnableRequestPriceAccept(record[0].status, user_id, record[0].client_id, record[0].contractor_id, record[0].price_in_negotiation) and record[0].price != int(request_price):
                model.requestPrice(accept_id, request.data.get('request_price'))
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
