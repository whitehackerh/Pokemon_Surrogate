import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Accepts import Accepts

class GetAcceptsService(BaseService):
    def service(self, request):
        try:
            status = request.data.get('status')
            user_id = request.user.id
            page = request.data.get('page')
            limit = 10
            offset = 0
            statuses = []
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            if status <= AcceptStatus.DELIVERED:
                statuses = [AcceptStatus.PRICE_NEGOTIATION, AcceptStatus.AWAITING_PAYMENT, AcceptStatus.AWAITING_DELIVERY, AcceptStatus.DELIVERED]
            else:
                statuses = [AcceptStatus.COMPLETED, AcceptStatus.CANCELLED]
            if page > 1:
                offset = ((page - 1) * limit)
            records = None
            model = Accepts()
            if request.data.get('client'):
                records = model.getAccepts(offset, limit, statuses, user_id, None)
            else:
                records = model.getAccepts(offset, limit, statuses, None, user_id)
            if not records:
                return {
                    'accepts': []
                }
            return self.__formatResponseData(records)
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        data = {}
        data['accepts'] = []
        for record in records:
            accept = {
                'picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.path)),
                'accept_id': record.id,
                'request_title': record.request_title,
                'game_title': record.game_title,
            }
            if record.status != AcceptStatus.PRICE_NEGOTIATION and record.price:
                accept['price'] = record.price 
            else:
                accept['min_price'] = record.min_price
                accept['max_price'] = record.max_price
            data['accepts'].append(accept)
        return data