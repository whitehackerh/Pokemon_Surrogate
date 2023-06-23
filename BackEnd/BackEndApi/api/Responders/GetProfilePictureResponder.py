from api.Responders.BaseResponder import BaseResponder

class GetProfilePictureResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getProfilePicture', exception)