from django.urls import path
from api.views import TestAPIView
from api.Views.SignupStaffView import SignupStaffView
from api.Views.SignupView import SignupView
from api.Views.LoginView import LoginView
from api.Views.LogoutView import LogoutView
from api.Views.GetUserProfileView import GetUserProfileView
from api.Views.SetUserProfileView import SetUserProfileView

urlpatterns = [
    path('test', TestAPIView.as_view(), name='test'),
    path('signupStaff', SignupStaffView.as_view(), name='signupStaff'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('getUserProfile', GetUserProfileView.as_view(), name='getUserProfile'),
    path('setUserProfile', SetUserProfileView.as_view(), name='setUserProfile')
]