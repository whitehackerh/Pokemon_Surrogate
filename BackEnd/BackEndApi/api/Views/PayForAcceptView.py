from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.PayForAcceptValidator import PayForAcceptValidator
from api.Services.PayForAcceptService import PayForAcceptService
from api.Responders.PayForAcceptResponder import PayForAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class PayForAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = PayForAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = PayForAcceptService()
            data = service.service(request)
            responder = PayForAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = PayForAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()