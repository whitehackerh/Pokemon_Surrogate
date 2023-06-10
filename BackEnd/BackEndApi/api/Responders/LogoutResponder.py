from api.Responders.BaseResponder import BaseResponder

class LogoutResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('logout', exception)