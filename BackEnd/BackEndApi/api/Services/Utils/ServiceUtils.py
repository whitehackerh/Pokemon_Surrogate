import base64
import os
from api.Enums.ListingStatus import ListingStatus
from api.Enums.ListingCategory import ListingCategory
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Enums.RequestStatus import RequestStatus
from api.Enums.AcceptStatus import AcceptStatus
from api.Models.Listings import Listings
from api.Models.Requests import Requests

class ServiceUtils:
    def makeDir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def getListingStatus(code):
        if code == ListingStatus.SELLING:
            return 'selling'
        elif code == ListingStatus.IN_PROGRESS:
            return 'in progress'
        elif code == ListingStatus.SOLD:
            return 'sold'
        elif code == ListingStatus.REMOVED:
            return 'removed'
    
    def getListingCategory(code):
        if code == ListingCategory.POKEMON:
            return 'Pokémon'
        elif code == ListingCategory.ITEMS:
            return 'Items'
        elif code == ListingCategory.SAVE_DATA:
            return 'Save Data'
        elif code == ListingCategory.BOOSTING:
            return 'Boosting'
        
    def getBase64FromPath(path):
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as file:
                return base64.b64encode(file.read()).decode('utf-8')
        else:
            raise FileNotFoundError(f"File not found at '{path}'.")
    
    def isEnableUpdateListing(listing_id, seller_id):
        model = Listings()
        record = model.getListingDetail(listing_id)
        return record.count() == 1 and record[0].seller_id == int(seller_id) and record[0].status == ListingStatus.SELLING
    
    def isEnableCancelPurchaseRequest(status):
        return status == PurchaseRequestStatus.AWAITING_PAYMENT or status == PurchaseRequestStatus.AWAITING_DELIVERY
    
    def isEnableRequestChangePricePurchaseRequest(price_negotiation, status, user_id, seller_id, buyer_id):
        if not price_negotiation:
            return False
        if user_id == seller_id:
            return False
        elif user_id == buyer_id:
            return status == PurchaseRequestStatus.AWAITING_PAYMENT
        else:
            return None
        
    def isEnableResponseChangePricePurchaseRequest(status, user_id, seller_id, buyer_id):
        if user_id == seller_id:
            return status == PurchaseRequestStatus.PRICE_NEGOTIATION
        elif user_id == buyer_id:
            return False
        else:
            return None
    
    def isEnablePaymentPurchaseRequest(status, user_id, seller_id, buyer_id):
        if user_id == seller_id:
            return False
        elif user_id == buyer_id:
            return status == PurchaseRequestStatus.AWAITING_PAYMENT
        else:
            return None
    
    def isEnableDeliverPurchaseRequest(status, user_id, seller_id, buyer_id):
        if user_id == seller_id:
            return status == PurchaseRequestStatus.AWAITING_DELIVERY
        elif user_id == buyer_id:
            return False
        else:
            return None
        
    def isEnableCompletePurchaseRequest(status, user_id, seller_id, buyer_id):
        if user_id == seller_id:
            return False
        elif user_id == buyer_id:
            return status == PurchaseRequestStatus.DELIVERED
        else:
            return None
    
    def isEnableSendMessagePurchaseRequest(status):
        return status <= PurchaseRequestStatus.DELIVERED

    def getUserId(request):
        if request.user is not None and request.user.id:
            return request.user.id
        else:
            return None
        
    def isEnableUpdateRequest(request_id, client_id):
        model = Requests()
        record = model.getRequestDetail(request_id)
        return record.count() == 1 and record[0].client_id == client_id and record[0].status == RequestStatus.ACCEPTING
    
    def isEnableCancelAccept(status, price_in_negotiation):
        return (status == AcceptStatus.PRICE_NEGOTIATION and not price_in_negotiation) or status == AcceptStatus.AWAITING_PAYMENT or status == AcceptStatus.AWAITING_DELIVERY
    
    def isEnableRequestChangePriceAccept(status, user_id, client_id, contractor_id, price_in_negotiation):
        if user_id == client_id:
            return (status == AcceptStatus.PRICE_NEGOTIATION and not price_in_negotiation) or status == AcceptStatus.AWAITING_PAYMENT
        elif user_id == contractor_id:
            return False
        else:
            return False
        
    def isEnableResponseChangePriceAccept(status, user_id, client_id, contractor_id, price_in_negotiation):
        if user_id == client_id:
            return False
        elif user_id == contractor_id and price_in_negotiation:
            return status == AcceptStatus.PRICE_NEGOTIATION
        else:
            return False
    
    def isEnablePaymentAccept(status, user_id, client_id, contractor_id):
        if user_id == client_id:
            return status == AcceptStatus.AWAITING_PAYMENT
        elif user_id == contractor_id:
            return False
        else:
            return None
    
    def isEnableDeliverAccept(status, user_id, client_id, contractor_id):
        if user_id == client_id:
            return False
        elif user_id == contractor_id:
            return status == AcceptStatus.AWAITING_DELIVERY
        else:
            return None
        
    def isEnableCompleteAccept(status, user_id, client_id, contractor_id):
        if user_id == client_id:
            return status == AcceptStatus.DELIVERED
        elif user_id == contractor_id:
            return False
        else:
            return None
    
    def isEnableSendMessageAccept(status):
        return status <= AcceptStatus.DELIVERED