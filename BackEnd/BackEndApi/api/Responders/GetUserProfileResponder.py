from api.Responders.BaseResponder import BaseResponder

class GetUserProfileResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getUserProfile', exception)