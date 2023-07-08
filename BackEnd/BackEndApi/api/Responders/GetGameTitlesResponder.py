from api.Responders.BaseResponder import BaseResponder

class GetGameTitlesResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('getGameTitles', exception)