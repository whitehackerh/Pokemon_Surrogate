from api.Responders.BaseResponder import BaseResponder

class LoginResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('login', exception)