import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.models import Users
from api.Enums.Path import Path

class SetProfilePictureService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            id = request.data.get('id')
            model = Users()
            currentPath = model.getUserProfile(request.data.get('id')).profile_picture
            ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.PROFILE_PICTURE))
            if request.data.get('delete') == True:
                model.setProfilePicture(id, Path.DEFAULT_PROFILE_PICTURE)
                self.__deleteProfilePicture(currentPath)
            else:
                filename = f"{id}_{uuid.uuid4().hex}.png"
                while filename == os.path.basename(currentPath):
                    filename = f"{id}_{uuid.uuid4().hex}.png"
                updatePath = os.path.join(Path.PROFILE_PICTURE, filename)
                model.setProfilePicture(id, updatePath)
                with open(os.path.join(settings.MEDIA_ROOT, updatePath), 'wb') as f:
                    for chunk in request.FILES.get('picture').chunks():
                        f.write(chunk)
                self.__deleteProfilePicture(currentPath)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def __deleteProfilePicture(self, currentPath):
        targetPath = os.path.join(settings.MEDIA_ROOT, currentPath)
        if currentPath != Path.DEFAULT_PROFILE_PICTURE and os.path.exists(targetPath):
            os.remove(targetPath)
