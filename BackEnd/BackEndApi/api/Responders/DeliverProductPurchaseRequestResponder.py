from api.Responders.BaseResponder import BaseResponder

class DeliverProductPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('deliverProductPurchaseRequest', exception)