"""youtubeApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from youtubeApp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view, name="home"),
    url(r'^authorize/$', authorize, name="authorize"),
    url(r'^oauth2callback$', oauth_callback_request, name="ouath_callback"),
    url(r'^ajax/channel_stats/$', channel_stats_ajax, name="channel_stats_ajax"),
    url(r'^ajax/upload_video/$', upload_ajax, name="upload_ajax"),
]
