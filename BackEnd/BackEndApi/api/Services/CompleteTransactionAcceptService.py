from django.db import transaction
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.AcceptStatus import AcceptStatus
from api.Enums.RequestStatus import RequestStatus
from api.Models.Accepts import Accepts
from api.Models.Requests import Requests

class CompleteTransactionAcceptService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            accept_id = request.data.get('accept_id')
            user_id = ServiceUtils.getUserId(request)
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            acceptsModel = Accepts()
            record = acceptsModel.getAcceptDetail(accept_id)
            if record.count() == 1 and ServiceUtils.isEnableCompleteAccept(record[0].status, user_id, record[0].client_id, record[0].contractor_id):
                acceptsModel.updateStatus(accept_id, AcceptStatus.COMPLETED)
                requestsModel = Requests()
                requestsModel.updateRequestStatus(record[0].request_id, RequestStatus.COMPLETE)
            else:
                raise CustomExceptions('Invalid Data.', ResponseCodes.INVALID_DATA)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
