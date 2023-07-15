import base64
import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.models import Users
from api.Enums.Path import Path

class GetProfilePictureService(BaseService):
    def service(self, request):
        try:
            data = {}
            model = Users()
            record = model.getUserProfile(request.get('id'))
            data['picture'] = ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, record.profile_picture))
            data['default'] = record.profile_picture == Path.DEFAULT_PROFILE_PICTURE
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)