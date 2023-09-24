import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.Accepts import Accepts
from api.Models.RequestPictures import RequestPictures

class GetAcceptDetailService(BaseService):
    def service(self, request):
        try:
            data = {}
            user_id = request.user.id
            if not user_id:
                raise CustomExceptions('Invalid Data', ResponseCodes.INVALID_DATA)
            accept_id = request.data.get('accept_id')
            acceptsModel = Accepts()
            requestPicturesModel = RequestPictures()
            accept = acceptsModel.getAcceptDetail(accept_id)
            if accept.count() == 1:
                requestPictures = requestPicturesModel.getRequestPictures(accept[0].request_id)
                data = self.__formatResponseData(user_id, accept_id, accept[0], requestPictures)
            else:
                data = None
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, user_id, accept_id, accept, requestPictures):
        data = {}
        pictures = []
        for requestPicture in requestPictures:
            pictures.append(ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, requestPicture.path)))
        if user_id == accept.client_id or user_id == accept.contractor_id:
            data = {
                'accept_id': accept_id,
                'client': {
                    'id': accept.client_id,
                    'profile_picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, accept.client_profile_picture)),
                    'nickname': accept.client_nickname
                },
                'contractor': {
                    'id': accept.contractor_id,
                    'profile_picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, accept.contractor_profile_picture)),
                    'nickname': accept.contractor_nickname
                },
                'status': accept.status,
                'game': {
                    'id': accept.game_title_id,
                    'title': accept.game_title
                },
                'category': {
                    'id': accept.category,
                    'name': ServiceUtils.getListingCategory(accept.category),
                },
                'request_title': accept.request_title,
                'description': accept.description,
                'price': accept.price,
                'price_in_negotiation': accept.price_in_negotiation,
                'price_range': {
                    'min': accept.min_price,
                    'max': accept.max_price
                },
                'fee': {
                    'id': accept.fee_id,
                    'percentage': accept.fee_percentage
                },
                'request_pictures': pictures,
                'enables': {
                    'cancel': ServiceUtils.isEnableCancelAccept(accept.status, accept.price_in_negotiation),
                    'request_price': ServiceUtils.isEnableRequestPriceAccept(accept.status, user_id, accept.client_id, accept.contractor_id, accept.price_in_negotiation),
                    'response_price': ServiceUtils.isEnableResponsePriceAccept(accept.status, user_id, accept.client_id, accept.contractor_id, accept.price_in_negotiation),
                    'payment': ServiceUtils.isEnablePaymentAccept(accept.status, user_id, accept.client_id, accept.contractor_id),
                    'deliver': ServiceUtils.isEnableDeliverAccept(accept.status, user_id, accept.client_id, accept.contractor_id),
                    'complete': ServiceUtils.isEnableCompleteAccept(accept.status, user_id, accept.client_id, accept.contractor_id),
                    'send_message': ServiceUtils.isEnableSendMessageAccept(accept.status)
                }
            }
        else:
            return None
        return data