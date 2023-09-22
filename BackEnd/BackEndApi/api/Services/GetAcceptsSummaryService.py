from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Accepts import Accepts

class GetAcceptsSummaryService(BaseService):
    def service(self, request):
        try:
            model = Accepts()
            status = int(request.data.get('status'))
            user_id = request.user.id
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            count = 0
            statuses = []
            if status <= AcceptStatus.DELIVERED:
                statuses = [AcceptStatus.PRICE_NEGOTIATION, AcceptStatus.AWAITING_PAYMENT, AcceptStatus.AWAITING_DELIVERY, AcceptStatus.DELIVERED]
            else:
                statuses = [AcceptStatus.COMPLETED, AcceptStatus.CANCELLED]
            if request.data.get('client'):
                count = model.getAcceptsRecordsCount(statuses, user_id, None)
            else:
                count = model.getAcceptsRecordsCount(statuses, None, user_id)
            return self.__formatResponseData(count)
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, count):
        data = {}
        data['count'] = count
        if count == 0:
            data['pages'] = 0
        elif count % 10 == 0:
            data['pages'] = count // 10
        else:
            data['pages'] = count // 10 + 1
        return data