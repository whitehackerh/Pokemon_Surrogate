from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.models import Users

class GetUserProfileService(BaseService):
    def service(self, request):
        try:
            id = request.get('id')
            model = Users()
            record = model.getUserProfile(id)
            data = {
                'id': id,
                'username': record.username,
                'first_name': record.first_name,
                'last_name': record.last_name,
                'email': record.email,
                'is_staff': record.is_staff,
                'nickname': record.nickname,
                'bank_account': record.bank_account
            }
            return data
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
