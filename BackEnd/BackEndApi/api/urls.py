from django.urls import path
from api.views import TestAPIView
from api.Views.SignupView import SignupView
from api.Views.LoginView import LoginView

urlpatterns = [
    path('test', TestAPIView.as_view(), name='test'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login')
]