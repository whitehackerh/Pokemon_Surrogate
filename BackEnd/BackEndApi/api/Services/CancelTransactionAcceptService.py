from django.db import transaction
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Enums.RequestStatus import RequestStatus
from api.Models.Accepts import Accepts
from api.Models.Requests import Requests

class CancelTransactionAcceptService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            acceptsModel = Accepts()
            record = acceptsModel.getAcceptDetail(accept_id)
            if record.count() == 1 and (user_id == record[0].client_id or user_id == record[0].contractor_id) and ServiceUtils.isEnableCancelAccept(record[0].status):
                acceptsModel.updateStatus(accept_id, AcceptStatus.CANCELLED)
                requestsModel = Requests()
                requestsModel.updateRequestStatus(record[0].request_id, RequestStatus.REMOVED)
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
