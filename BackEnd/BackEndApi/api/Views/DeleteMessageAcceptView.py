from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.DeleteMessageAcceptValidator import DeleteMessageAcceptValidator
from api.Services.DeleteMessageAcceptService import DeleteMessageAcceptService
from api.Responders.DeleteMessageAcceptResponder import DeleteMessageAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class DeleteMessageAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = DeleteMessageAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = DeleteMessageAcceptService()
            data = service.service(request)
            responder = DeleteMessageAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = DeleteMessageAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()