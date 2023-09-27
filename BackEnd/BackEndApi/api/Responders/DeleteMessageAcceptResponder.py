from api.Responders.BaseResponder import BaseResponder

class DeleteMessageAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('deleteMessageAccept', exception)