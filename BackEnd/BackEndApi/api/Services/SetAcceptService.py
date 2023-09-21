from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.RequestStatus import RequestStatus
from api.Enums.AcceptStatus import AcceptStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Requests import Requests
from api.models import Users
from api.Models.Accepts import Accepts

class SetAcceptService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            data = {}
            request_id = request.data.get('request_id')
            contractor_id = request.user.id
            if not contractor_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)

            requestsModel = Requests()
            usersModel = Users()
            requestRecord = requestsModel.getRequestDetail(request_id)
            if requestRecord.count() == 1 and usersModel.getUserProfile(contractor_id).id == contractor_id and requestRecord[0].client_id != contractor_id and ServiceUtils.isEnableUpdateRequest(request_id, requestRecord[0].client_id):
                acceptsModel = Accepts(**{
                    'request_id': requestRecord[0].id,
                    'client_id': requestRecord[0].client_id,
                    'contractor_id': contractor_id,
                    'status': AcceptStatus.PRICE_NEGOTIATION
                })
                acceptsModel.save()
                requestsModel.updateRequestStatus(request_id, RequestStatus.IN_PROGRESS)
                data['accept_id'] = acceptsModel.id
            else:
                raise CustomExceptions('Invalid Data', ResponseCodes.INTERNAL_SERVER_ERROR)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)