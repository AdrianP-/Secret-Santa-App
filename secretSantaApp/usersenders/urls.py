from django.conf.urls import url
from usersenders.views import UserSenderRegistrationAPIView
from usersenders.views import UserSenderGifteeAPIView

urlpatterns = [
    url(r'^$', UserSenderRegistrationAPIView.as_view(), name="register"),
    url(r'^getGiftee/', UserSenderGifteeAPIView.as_view(), name="getGiftee")
]