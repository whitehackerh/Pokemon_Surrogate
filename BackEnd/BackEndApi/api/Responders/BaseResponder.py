from rest_framework.response import Response
from datetime import datetime

class BaseResponder:
    def __init__(self, api_name, e = None):
        self.responseParameter = {}
        self.statusCode = 200
        self.apiName = api_name
        self.successful = 'success'
        self.responseCode = '000'
        self.data = {}

        if e:
            self.statusCode = 400
            self.successful = 'failure'
            self.responseCode = e['code']
            self.data['errors'] = e['message']
        
    def setResponse(self, data=None):
        self.responseParameter['responseCode'] = self.responseCode
        self.responseParameter['time'] = self.getTime()
        self.responseParameter['apiname'] = self.apiName
        self.responseParameter['successful'] = self.successful
        if self.successful == 'success':
            self.responseParameter['data'] = data
        else:
            self.responseParameter['data'] = self.data
    
    def getResponse(self):
        return Response(self.responseParameter, self.statusCode)

    def getTime(self):
        return datetime.now().strftime("%m-%d-%Y %H:%M:%S")

