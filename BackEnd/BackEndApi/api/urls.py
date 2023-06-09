from django.urls import path
from api.views import TestAPIView
from api.Views.SignupStaffView import SignupStaffView
from api.Views.SignupView import SignupView
from api.Views.LoginView import LoginView
from api.Views.LogoutView import LogoutView
from api.Views.GetUserProfileView import GetUserProfileView
from api.Views.SetUserProfileView import SetUserProfileView
from api.Views.GetProfilePictureView import GetProfilePictureView
from api.Views.SetProfilePictureView import SetProfilePictureView
from api.Views.SetListingView import SetListingView
from api.Views.GetGameTitlesView import GetGameTitlesView
from api.Views.GetAvailableFeeView import GetAvailableFeeView

urlpatterns = [
    path('signupStaff', SignupStaffView.as_view(), name='signupStaff'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('getUserProfile', GetUserProfileView.as_view(), name='getUserProfile'),
    path('setUserProfile', SetUserProfileView.as_view(), name='setUserProfile'),
    path('getProfilePicture', GetProfilePictureView.as_view(), name='getProfilePicture'),
    path('setProfilePicture', SetProfilePictureView.as_view(), name='setProfilePicture'),
    path('setListing', SetListingView.as_view(), name='setListing'),
    path('getGameTitles', GetGameTitlesView.as_view(), name='getGameTitles'),
    path('getAvailableFee', GetAvailableFeeView.as_view(), name='getAvailableFee')
]