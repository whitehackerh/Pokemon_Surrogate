from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.RequestStatus import RequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.Requests import Requests

class GetRequestsSummaryService(BaseService):
    def service(self, request):
        try:
            model = Requests()
            count = 0
            status = request.data.get('status')
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
                    count = model.getRequestsPersonalCount(client_id, statuses)
                else:
                    raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            else:
                count = model.getRequestsPublicCount()
            return self.__formatResponseData(count)
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, count):
        pages = None
        if count == 0:
            pages = 0
        elif count % 10 == 0:
            pages = count // 10
        else:
            pages = count // 10 + 1
        return {
            'count': count,
            'pages': pages
        }