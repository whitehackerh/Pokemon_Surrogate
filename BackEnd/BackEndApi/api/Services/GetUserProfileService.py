from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.models import Users

class GetUserProfileService(BaseService):
    def service(self, request):
        try:
            data = {}
            id = request.get('id')
            model = Users()
            record = model.getUserProfile(id)
            data = self.__formatResponseData(id, record)
            return data
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def __formatResponseData(self, id, record):
        return {
            'id': id,
            'username': record.username,
            'first_name': record.first_name,
            'last_name': record.last_name,
            'email': record.email,
            'is_staff': record.is_staff,
            'nickname': record.nickname,
            'bank_account': record.bank_account
        }
