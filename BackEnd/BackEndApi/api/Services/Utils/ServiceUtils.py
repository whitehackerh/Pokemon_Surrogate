import base64
import os
from api.Enums.ListingStatus import ListingStatus
from api.Enums.ListingCategory import ListingCategory
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