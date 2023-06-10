from django.urls import path
from api.views import TestAPIView
from api.Views.SignupView import SignupView

urlpatterns = [
    path('test', TestAPIView.as_view(), name='/test'),
    path('signup', SignupView.as_view(), name='/signup')
]