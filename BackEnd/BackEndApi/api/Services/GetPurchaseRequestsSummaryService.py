from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.PurchaseRequests import PurchaseRequests

class GetPurchaseRequestsSummaryService(BaseService):
    def service(self, request):
        try:
            data = {}
            model = PurchaseRequests()
            status = int(request.get('status'))
            seller_id = request.get('seller_id')
            buyer_id = request.get('buyer_id')
            count = 0
            statuses = []
            if status <= PurchaseRequestStatus.AWAITING_DELIVERY:
                statuses = [PurchaseRequestStatus.PRICE_NEGOTIATION, PurchaseRequestStatus.AWAITING_PAYMENT, PurchaseRequestStatus.AWAITING_DELIVERY]
            else:
                statuses = [PurchaseRequestStatus.COMPLETED, PurchaseRequestStatus.CANCELLED]
            if seller_id:
                count = model.getPurchaseRequestsRecordsCount(statuses, seller_id, None)
            elif buyer_id:
                count = model.getPurchaseRequestsRecordsCount(statuses, None, buyer_id)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            data = self.__formatResponseData(count)
            return data
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