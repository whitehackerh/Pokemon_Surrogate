from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetRequestDetailValidator import GetRequestDetailValidator
from api.Services.GetRequestDetailService import GetRequestDetailService
from api.Responders.GetRequestDetailResponder import GetRequestDetailResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetRequestDetailView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = GetRequestDetailValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetRequestDetailService()
            data = service.service(request)
            responder = GetRequestDetailResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetRequestDetailResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()