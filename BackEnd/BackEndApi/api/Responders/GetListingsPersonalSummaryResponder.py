from api.Responders.BaseResponder import BaseResponder

class GetListingsPersonalSummaryResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getListingsPersonalSummary', exception)