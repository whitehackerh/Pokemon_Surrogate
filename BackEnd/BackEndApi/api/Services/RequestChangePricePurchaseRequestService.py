from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Models.PurchaseRequests import PurchaseRequests

class RequestChangePricePurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchase_request_id = request.get('purchase_request_id')
            request_price = request.get('request_price')
            model = PurchaseRequests()
            record = model.getPurchaseRequestDetail(purchase_request_id)
            if record.count() == 1 and ServiceUtils.isEnableRequestChangePricePurchaseRequest(record[0].status, int(request.get('buyer_id')), record[0].seller_id, record[0].buyer_id) and record[0].price != int(request_price):
                model.requestChangePrice(purchase_request_id, request.get('request_price'))
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
