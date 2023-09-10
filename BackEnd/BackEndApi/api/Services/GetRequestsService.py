import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.RequestStatus import RequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Requests import Requests

class GetRequestsService(BaseService):
    def service(self, request):
        try:
            model = Requests()
            status = request.data.get('status')
            page = request.data.get('page')
            limit = 10
            offset = 0
            if page > 1:
                offset = ((page - 1) * limit)
            records = None
            if request.user is not None and request.user.id:
                if status != None and (status >= RequestStatus.ACCEPTING and status <= RequestStatus.REMOVED):
                    client_id = request.user.id
                    statuses = []
                    if status == RequestStatus.ACCEPTING:
                        statuses = [status]
                    elif status == RequestStatus.COMPLETE:
                        statuses = [status, RequestStatus.REMOVED]
                    else:
                        raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
                    records = model.getRequestsPersonal(client_id, statuses, offset, limit)
                else:
                    raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            else:
                records = model.getRequestsPublic(offset, limit)
            return self.__formatResponseData(records)
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        requests = []
        for record in records:
            requests.append({
                'picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.path)),
                'request_id': record.id,
                'request_title': record.request_title,
                'game_title': record.game_title,
                'min_price': record.min_price,
                'max_price': record.max_price
            })
        return {
            'requests': requests
        }