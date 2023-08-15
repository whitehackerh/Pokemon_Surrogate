from api.Responders.BaseResponder import BaseResponder

class ResponseChangePricePurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('responseChangePricePurchaseRequest', exception)