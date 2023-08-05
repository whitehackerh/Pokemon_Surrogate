from api.Responders.BaseResponder import BaseResponder

class SetPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setPurchaseRequest', exception)