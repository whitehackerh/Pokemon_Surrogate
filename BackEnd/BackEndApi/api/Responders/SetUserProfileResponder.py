from api.Responders.BaseResponder import BaseResponder

class SetUserProfileResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setUserProfile', exception)