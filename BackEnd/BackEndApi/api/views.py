from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class TestAPIView(APIView):
    def get(self, request):
        # GETリクエストに対する処理
        data = {'message': 'This is a test API.'}
        return Response(data)