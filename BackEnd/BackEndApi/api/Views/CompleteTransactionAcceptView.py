from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.CompleteTransactionAcceptValidator import CompleteTransactionAcceptValidator
from api.Services.CompleteTransactionAcceptService import CompleteTransactionAcceptService
from api.Responders.CompleteTransactionAcceptResponder import CompleteTransactionAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class CompleteTransactionAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = CompleteTransactionAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = CompleteTransactionAcceptService()
            data = service.service(request)
            responder = CompleteTransactionAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = CompleteTransactionAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()