from django.urls import path
from api.views import TestAPIView
from api.Views.SignupView import SignupView
from api.Views.LoginView import LoginView
from api.Views.LogoutView import LogoutView
from api.Views.SetUserProfileView import SetUserProfileView
from api.Views.SignupStaffView import SignupStaffView

urlpatterns = [
    path('test', TestAPIView.as_view(), name='test'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('setUserProfile', SetUserProfileView.as_view(), name='setUserProfile'),
    path('signupStaff', SignupStaffView.as_view(), name='signupStaff')
]