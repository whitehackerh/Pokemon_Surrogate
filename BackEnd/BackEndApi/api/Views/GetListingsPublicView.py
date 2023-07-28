from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.GetListingsPublicValidator import GetListingsPublicValidator
from api.Services.GetListingsPublicService import GetListingsPublicService
from api.Responders.GetListingsPublicResponder import GetListingsPublicResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class GetListingsPublicView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            validator = GetListingsPublicValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = GetListingsPublicService()
            data = service.service(request.data)
            responder = GetListingsPublicResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = GetListingsPublicResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()