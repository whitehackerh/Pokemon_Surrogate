from api.Responders.BaseResponder import BaseResponder

class GetListingsPublicSummaryResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getListingsPublicSummary', exception)