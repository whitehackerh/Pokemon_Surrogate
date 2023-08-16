from api.Responders.BaseResponder import BaseResponder

class PayForPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('payForPurchaseRequest', exception)