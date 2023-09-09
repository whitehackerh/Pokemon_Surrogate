import os
import uuid
from django.conf import settings
from django.db import transaction
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Requests import Requests
from api.Models.RequestPictures import RequestPictures
from api.Enums.Path import Path
from api.Enums.RequestStatus import RequestStatus

class SetRequestService(BaseService):
    @transaction.atomic
    def service(self, request):
        try:
            if request.data.get('request_id'):
                self.__updateRequest(request)
            else: self.__createRequest(request)
            return None
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)

    def __createRequest(self, request):
        client_id = request.user.id
        if client_id:
            requestsModel = Requests(**{
                'client_id': client_id,
                'game_title_id': request.data.get('game_title_id'),
                'category': request.data.get('category'),
                'request_title': request.data.get('request_title'),
                'description': request.data.get('description'),
                'min_price': request.data.get('min_price'),
                'max_price': request.data.get('max_price'),
                'status': RequestStatus.ACCEPTING
            })
            requestsModel.save()

            request_id = requestsModel.id
            if not request.FILES:
                self.__registerDefaultPicture(request_id, client_id)
            else:
                ServiceUtils.makeDir(os.path.join(settings.MEDIA_ROOT, Path.REQUEST_PICTURE_DIR))
                requestPicturesParams = []
                for index in range(1, 11):
                    if f'picture{index}' in request.FILES:
                        filename = f'{request_id}_{uuid.uuid4().hex}.png'
                        while any(filename == os.path.basename(requestPicture['path']) for requestPicture in requestPicturesParams):
                            filename = f'{request_id}_{uuid.uuid4().hex}.png'
                        requestPicturesParams.append({
                            'request_id': request_id,
                            'client_id': client_id,
                            'path': os.path.join(Path.REQUEST_PICTURE_DIR, filename),
                            'sort_no': index
                        })
                RequestPictures.objects.bulk_create([RequestPictures(**requestPicturesParam) for requestPicturesParam in requestPicturesParams])
                for requestPicturesParam in requestPicturesParams:
                    with open(os.path.join(settings.MEDIA_ROOT, requestPicturesParam['path']), 'wb') as f:
                        for chunk in request.FILES.get(f"picture{requestPicturesParam['sort_no']}").chunks():
                            f.write(chunk)
        else:
            raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
        return None

    def __updateRequest(self, request):
        return None
    
    def __registerDefaultPicture(self, request_id, client_id):
        RequestPictures(**{
            'request_id': request_id,
            'client_id': client_id,
            'path': Path.LOGO,
            'sort_no': 1
        }).save()