from api.Responders.BaseResponder import BaseResponder

class CancelTransactionAcceptResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('cancelTransactionAccept', exception)