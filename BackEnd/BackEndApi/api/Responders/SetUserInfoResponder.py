from api.Responders.BaseResponder import BaseResponder

class SetUserInfoResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setUserInfo', exception)