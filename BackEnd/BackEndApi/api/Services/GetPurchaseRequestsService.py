import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.PurchaseRequests import PurchaseRequests

class GetPurchaseRequestsService(BaseService):
    def service(self, request):
        try:
            data = {}
            status = request.get('status')
            seller_id = request.get('seller_id')
            buyer_id = request.get('buyer_id')
            page = request.get('page')
            limit = 10
            offset = 0
            statuses = []
            if status <= PurchaseRequestStatus.DELIVERED:
                statuses = [PurchaseRequestStatus.PRICE_NEGOTIATION, PurchaseRequestStatus.AWAITING_PAYMENT, PurchaseRequestStatus.AWAITING_DELIVERY, PurchaseRequestStatus.DELIVERED]
            else:
                statuses = [PurchaseRequestStatus.COMPLETED, PurchaseRequestStatus.CANCELLED]
            if page > 1:
                offset = ((page - 1) * limit)
            records = None
            model = PurchaseRequests()
            if seller_id:
                records = model.getPurchaseRequests(offset, limit, statuses, seller_id, None)
            elif buyer_id:
                records = model.getPurchaseRequests(offset, limit, statuses, None, buyer_id)
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            if not records:
                data['purchaseRequests'] = []
                return data
            data = self.__formatResponseData(records)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        data = {}
        data['purchaseRequests'] = []
        for record in records:
            purchaseRequest = {
                'picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.path)),
                'purchase_request_id': record.id,
                'listing_title': record.listing_title,
                'game_title': record.game_title,
                'price': record.price
            }
            data['purchaseRequests'].append(purchaseRequest)
        return data