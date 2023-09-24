from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Models.Accepts import Accepts
from api.Models.Fees import Fees

class ResponsePriceAcceptService(BaseService):
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            acceptsModel = Accepts()
            record = acceptsModel.getAcceptDetail(accept_id)
            feesModel = Fees()
            fee_id = feesModel.getAvailableFee().id
            if record.count() == 1 and ServiceUtils.isEnableResponsePriceAccept(record[0].status, user_id, record[0].client_id, record[0].contractor_id, record[0].price_in_negotiation):
                acceptsModel.responseChangePrice(accept_id, request.data.get('response'), record[0].price_in_negotiation, fee_id)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
