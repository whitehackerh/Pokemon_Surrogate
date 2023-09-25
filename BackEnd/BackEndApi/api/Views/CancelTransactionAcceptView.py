from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.CancelTransactionAcceptValidator import CancelTransactionAcceptValidator
from api.Services.CancelTransactionAcceptService import CancelTransactionAcceptService
from api.Responders.CancelTransactionAcceptResponder import CancelTransactionAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class CancelTransactionAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = CancelTransactionAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = CancelTransactionAcceptService()
            data = service.service(request)
            responder = CancelTransactionAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = CancelTransactionAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()