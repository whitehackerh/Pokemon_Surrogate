from api.Responders.BaseResponder import BaseResponder

class SetProfilePictureResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('setProfilePicture', exception)