from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.RequestStatus import RequestStatus
from api.Models.Requests import Requests

class RemoveRequestService(BaseService):
    def service(self, request):
        try:
            request_id = request.data.get('request_id')
            client_id = ServiceUtils.getUserId(request)
            if client_id and ServiceUtils.isEnableUpdateRequest(request_id, client_id):
                model = Requests()
                model.updateRequestStatus(request_id, RequestStatus.REMOVED)
            else:
                raise CustomExceptions('Not Available.', ResponseCodes.INTERNAL_SERVER_ERROR)
            return None
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
