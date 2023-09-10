from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetRequestsValidator import GetRequestsValidator
from api.Services.GetRequestsService import GetRequestsService
from api.Responders.GetRequestsResponder import GetRequestsResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetRequestsView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = GetRequestsValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetRequestsService()
            data = service.service(request)
            responder = GetRequestsResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetRequestsResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()