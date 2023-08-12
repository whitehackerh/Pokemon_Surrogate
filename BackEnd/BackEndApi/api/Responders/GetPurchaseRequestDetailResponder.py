from api.Responders.BaseResponder import BaseResponder

class GetPurchaseRequestDetailResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getPurchaseRequestDetail', exception)