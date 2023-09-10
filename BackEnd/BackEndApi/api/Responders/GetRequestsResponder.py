from api.Responders.BaseResponder import BaseResponder

class GetRequestsResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getRequests', exception)