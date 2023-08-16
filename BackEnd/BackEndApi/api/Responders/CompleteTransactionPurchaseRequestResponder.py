from api.Responders.BaseResponder import BaseResponder

class CompleteTransactionPurchaseRequestResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('completeTransactionPurchaseRequest', exception)