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
from api.Views.GetListingsPersonalSummaryView import GetListingsPersonalSummaryView
from api.Views.GetListingsPersonalView import GetListingsPersonalView
from api.Views.GetListingDetailView import GetListingDetailView
from api.Views.GetListingsPublicSummaryView import GetListingsPublicSummaryView
from api.Views.GetListingsPublicView import GetListingsPublicView
from api.Views.RemoveListingView import RemoveListingView
from api.Views.SetPurchaseRequestView import SetPurchaseRequestView
from api.Views.GetPurchaseRequestsSummaryView import GetPurchaseRequestsSummaryView
from api.Views.GetPurchaseRequestsView import GetPurchaseRequestsView
from api.Views.GetPurchaseRequestDetailView import GetPurchaseRequestDetailView
from api.Views.RequestChangePricePurchaseRequestView import RequestChangePricePurchaseRequestView
from api.Views.ResponseChangePricePurchaseRequestView import ResponseChangePricePurchaseRequestView
from api.Views.PayForPurchaseRequestView import PayForPurchaseRequestView
from api.Views.DeliverProductPurchaseRequestView import DeliverProductPurchaseRequestView
from api.Views.CompleteTransactionPurchaseRequestView import CompleteTransactionPurchaseRequestView
from api.Views.CancelTransactionPurchaseRequestView import CancelTransactionPurchaseRequestView
from api.Views.SendMessagePurchaseRequestView import SendMessagePurchaseRequestView
from api.Views.GetMessagesPurchaseRequestView import GetMessagesPurchaseRequestView
from api.Views.SetReadMessagesPurchaseRequestView import SetReadMessagesPurchaseRequestView
from api.Views.DeleteMessagePurchaseRequestView import DeleteMessagePurchaseRequestView
from api.Views.SetRequestView import SetRequestView
from api.Views.GetRequestsSummaryView import GetRequestsSummaryView
from api.Views.GetRequestsView import GetRequestsView
from api.Views.GetRequestDetailView import GetRequestDetailView
from api.Views.RemoveRequestView import RemoveRequestView
from api.Views.SetAcceptView import SetAcceptView

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
    path('getAvailableFee', GetAvailableFeeView.as_view(), name='getAvailableFee'),
    path('getListingsPersonalSummary', GetListingsPersonalSummaryView.as_view(), name='getListingsPersonalSummary'),
    path('getListingsPersonal', GetListingsPersonalView.as_view(), name='getListingsPersonal'),
    path('getListingDetail', GetListingDetailView.as_view(), name='getListingDetail'),
    path('getListingsPublicSummary', GetListingsPublicSummaryView.as_view(), name='getListingsPublicSummary'),
    path('getListingsPublic', GetListingsPublicView.as_view(), name='getListingsPublic'),
    path('removeListing', RemoveListingView.as_view(), name='removeListing'),
    path('setPurchaseRequest', SetPurchaseRequestView.as_view(), name='setPurchaseRequest'),
    path('getPurchaseRequestsSummary', GetPurchaseRequestsSummaryView.as_view(), name='getPurchaseRequestsSummary'),
    path('getPurchaseRequests', GetPurchaseRequestsView.as_view(), name='getPurchaseRequests'),
    path('getPurchaseRequestDetail', GetPurchaseRequestDetailView.as_view(), name='getPurchaseRequestDetail'),
    path('requestChangePricePurchaseRequest', RequestChangePricePurchaseRequestView.as_view(), name='requestChangePricePurchaseRequest'),
    path('responseChangePricePurchaseRequest', ResponseChangePricePurchaseRequestView.as_view(), name='responseChangePricePurchaseRequest'),
    path('payForPurchaseRequest', PayForPurchaseRequestView.as_view(), name='payForPurchaseRequest'),
    path('deliverProductPurchaseRequest', DeliverProductPurchaseRequestView.as_view(), name='deliverProductPurchaseRequest'),
    path('completeTransactionPurchaseRequest', CompleteTransactionPurchaseRequestView.as_view(), name='completeTransactionPurchaseRequest'),
    path('cancelTransactionPurchaseRequest', CancelTransactionPurchaseRequestView.as_view(), name='cancelTransactionPurchaseRequest'),
    path('sendMessagePurchaseRequest', SendMessagePurchaseRequestView.as_view(), name='sendMessagePurchaseRequest'),
    path('getMessagesPurchaseRequest', GetMessagesPurchaseRequestView.as_view(), name='getMessagesPurchaseRequest'),
    path('setReadMessagesPurchaseRequest', SetReadMessagesPurchaseRequestView.as_view(), name='setReadMessagesPurchaseRequest'),
    path('deleteMessagePurchaseRequest', DeleteMessagePurchaseRequestView.as_view(), name='deleteMessagePurchaseRequest'),
    path('setRequest', SetRequestView.as_view(), name='setRequest'),
    path('getRequestsSummary', GetRequestsSummaryView.as_view(), name='getRequestsSummary'),
    path('getRequests', GetRequestsView.as_view(), name='getRequests'),
    path('getRequestDetail', GetRequestDetailView.as_view(), name='getRequestDetail'),
    path('removeRequest', RemoveRequestView.as_view(), name='removeRequest'),
    path('setAccept', SetAcceptView.as_view(), name='setAccept')
]