from django.conf.urls import url, include
from django.contrib import admin


api_urls = [
    url(r'^users/', include('usersenders.urls', namespace='usersenders')),
]

urlpatterns = [
    url(r'^api/', include(api_urls)),
]
