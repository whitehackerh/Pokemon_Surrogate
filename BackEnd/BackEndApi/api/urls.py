from django.urls import path
from api.views import TestAPIView

urlpatterns = [
    path('test', TestAPIView.as_view(), name='/test'),
]