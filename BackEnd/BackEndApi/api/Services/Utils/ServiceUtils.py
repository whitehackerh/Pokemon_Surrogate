import base64
import os
from api.Enums.ListingStatus import ListingStatus
from api.Enums.ListingCategory import ListingCategory
from api.Enums.PurchaseRequestStatus import PurchaseRequestStatus
from api.Models.Listings import Listings

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
    
    def isEnableRequestChangePricePurchaseRequest(status, user_id, seller_id, buyer_id):
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