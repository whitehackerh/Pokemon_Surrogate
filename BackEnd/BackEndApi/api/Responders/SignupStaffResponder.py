from api.Responders.BaseResponder import BaseResponder

class SignupStaffResponder(BaseResponder):
    def __init__(self, exception = None):
        super().__init__('signupStaff', exception)