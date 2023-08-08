from api.Responders.BaseResponder import BaseResponder

class GetPurchaseRequestsSummaryResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getPurchaseRequestsSummary', exception)