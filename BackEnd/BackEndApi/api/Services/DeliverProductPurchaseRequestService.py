from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Models.PurchaseRequests import PurchaseRequests

class DeliverProductPurchaseRequestService(BaseService):
    def service(self, request):
        try:
            purchase_request_id = request.get('purchase_request_id')
            model = PurchaseRequests()
            record = model.getPurchaseRequestDetail(purchase_request_id)
            if record.count() == 1 and ServiceUtils.isEnableDeliverPurchaseRequest(record[0].status, int(request.get('seller_id')), record[0].seller_id, record[0].buyer_id):
                model.updateStatus(purchase_request_id, PurchaseRequestStatus.DELIVERED)
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
