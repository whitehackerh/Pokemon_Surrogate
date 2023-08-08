from api.Responders.BaseResponder import BaseResponder

class GetPurchaseRequestsResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getPurchaseRequests', exception)