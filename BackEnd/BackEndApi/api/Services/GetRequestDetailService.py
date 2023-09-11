import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Requests import Requests
from api.Models.RequestPictures import RequestPictures
from api.Enums.RequestStatus import RequestStatus
from api.Enums.Path import Path

class GetRequestDetailService(BaseService):
    def service(self, request):
        try:
            request_id = request.data.get('request_id')
            requestsModel = Requests()
            requestPicturesModel = RequestPictures()
            requestRecord = requestsModel.getRequestDetail(request_id)
            requestPictures = requestPicturesModel.getRequestPictures(request_id)
            if requestRecord.count() == 1:
                data = self.__formatResponseData(ServiceUtils.getUserId(request), request_id, requestRecord[0], requestPictures)
            else:
                data = None
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, user_id, request_id, request, requestPictures):
        pictures = []
        for requestPicture in requestPictures:
            pictures.append(ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, requestPicture.path)))
        defaultPicture = False
        if requestPictures.count() == 1 and requestPictures[0].path == Path.LOGO:
            defaultPicture = True            
        return {
            'request_id': request_id,
            'client': {
                'user_id': request.client_id,
                'profile_picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, request.clients_profile_picture)),
                'nickname': request.nickname
            },
            'status': request.status,
            'enables': {
                'edit': request.client_id == user_id and request.status == RequestStatus.ACCEPTING,
                'accept': user_id != None and user_id != request.client_id and request.status == RequestStatus.ACCEPTING
            },
            'game': {
                'id': request.game_title_id,
                'title': request.game_title
            },
            'category': {
                'id': request.category,
                'name': ServiceUtils.getListingCategory(request.category)
            },
            'request_title': request.request_title,
            'description': request.description,
            'min_price': request.min_price,
            'max_price': request.max_price,
            'pictures': pictures,
            'default_picture': defaultPicture
        }