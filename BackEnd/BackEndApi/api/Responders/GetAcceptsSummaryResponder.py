from api.Responders.BaseResponder import BaseResponder

class GetAcceptsSummaryResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getAcceptsSummary', exception)