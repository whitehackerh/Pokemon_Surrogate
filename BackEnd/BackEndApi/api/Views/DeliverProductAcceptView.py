from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.Validators.DeliverProductAcceptValidator import DeliverProductAcceptValidator
from api.Services.DeliverProductAcceptService import DeliverProductAcceptService
from api.Responders.DeliverProductAcceptResponder import DeliverProductAcceptResponder
from api.Exceptions.CustomExceptions import CustomExceptions

class DeliverProductAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validator = DeliverProductAcceptValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            service = DeliverProductAcceptService()
            data = service.service(request)
            responder = DeliverProductAcceptResponder()
            responder.setResponse(data)
            return responder.getResponse()
        except CustomExceptions as e:
            responder = DeliverProductAcceptResponder({'message': e.message, 'code': e.code})
            responder.setResponse()
            return responder.getResponse()