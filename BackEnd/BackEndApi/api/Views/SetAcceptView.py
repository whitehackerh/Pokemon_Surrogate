from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.SetAcceptValidator import SetAcceptValidator
from api.Services.SetAcceptService import SetAcceptService
from api.Responders.SetAcceptResponder import SetAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class SetAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = SetAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = SetAcceptService()
            data = service.service(request)
            responder = SetAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = SetAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()