import os
from django.conf import settings
from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Services.Utils.ServiceUtils import ServiceUtils
from api.Models.PurchaseRequests import PurchaseRequests
from api.Models.ListingPictures import ListingPictures

class GetPurchaseRequestDetailService(BaseService):
    def service(self, request):
        try:
            data = {}
            purchase_request_id = request.get('purchase_request_id')
            purchaseRequestsModel = PurchaseRequests()
            listingPicturesModel = ListingPictures()
            purchase_request = purchaseRequestsModel.getPurchaseRequestDetail(purchase_request_id)
            if purchase_request.count() == 1:
                listingPictures = listingPicturesModel.getListingPictures(purchase_request[0].listing_id)
                data = self.__formatResponseData(request.get('user_id'), purchase_request_id, purchase_request[0], listingPictures)
            else:
                data = None
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, user_id, purchase_request_id, purchase_request, listingPictures):
        data = {}
        user_id = int(user_id)
        pictures = []
        for listingPicture in listingPictures:
            pictures.append(ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, listingPicture.path)))
        if user_id == purchase_request.seller_id or user_id == purchase_request.buyer_id:
            data = {
                'purchase_request_id': purchase_request_id,
                'seller_id': purchase_request.seller_id,
                'seller_profile_picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, purchase_request.seller_profile_picture)),
                'seller_nickname': purchase_request.seller_nickname,
                'buyer_id': purchase_request.buyer_id,
                'buyer_profile_picture': ServiceUtils.getBase64FromPath(os.path.join(settings.MEDIA_ROOT, purchase_request.buyer_profile_picture)),
                'buyer_nickname': purchase_request.buyer_nickname,
                'status': purchase_request.status,
                'game_title_id': purchase_request.game_title_id,
                'game_title': purchase_request.game_title,
                'category_id': purchase_request.category,
                'category': ServiceUtils.getListingCategory(purchase_request.category),
                'listing_title': purchase_request.listing_title,
                'description': purchase_request.description,
                'price': purchase_request.price,
                'price_negotiation': purchase_request.price_negotiation,
                'price_in_negotiation': purchase_request.price_in_negotiation,
                'fee_id': purchase_request.fee_id,
                'fee_percentage': purchase_request.fee_percentage,
                'listing_pictures': pictures,
                'enable_cancel': ServiceUtils.isEnableCancelPurchaseRequest(purchase_request.status),
                'enable_request_change_price': ServiceUtils.isEnableRequestChangePricePurchaseRequest(purchase_request.price_negotiation, purchase_request.status, user_id, purchase_request.seller_id, purchase_request.buyer_id),
                'enable_response_change_price': ServiceUtils.isEnableResponseChangePricePurchaseRequest(purchase_request.status, user_id, purchase_request.seller_id, purchase_request.buyer_id),
                'enable_payment': ServiceUtils.isEnablePaymentPurchaseRequest(purchase_request.status, user_id, purchase_request.seller_id, purchase_request.buyer_id),
                'enable_deliver': ServiceUtils.isEnableDeliverPurchaseRequest(purchase_request.status, user_id, purchase_request.seller_id, purchase_request.buyer_id),
                'enable_complete': ServiceUtils.isEnableCompletePurchaseRequest(purchase_request.status, user_id, purchase_request.seller_id, purchase_request.buyer_id),
                'enable_send_message': ServiceUtils.isEnableSendMessagePurchaseRequest(purchase_request.status)
            }
        else:
            return None
        return data