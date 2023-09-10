from api.Responders.BaseResponder import BaseResponder

class GetRequestsSummaryResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getRequestsSummary', exception)