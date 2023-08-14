from api.Responders.BaseResponder import BaseResponder

class RequestChangePricePurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('requestChangePricePurchaseRequest', exception)