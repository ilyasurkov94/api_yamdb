from django.urls import path

from .views import UserCreateOrSendMailCodeAPI, UserEmailCodeLoginAPI


urlpatterns = [
    path('signup/', UserCreateOrSendMailCodeAPI.as_view()),
    path('token/', UserEmailCodeLoginAPI.as_view()),
]
