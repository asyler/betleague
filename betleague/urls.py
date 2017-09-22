"""betleague URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

import accounts.urls as accounts_urls
import matches.views as matches_views
from competitions.views import matches
from competitions.views import league

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^my_bets', matches_views.user_bets, name='user_bets'),
    url(r'^matches', matches, name='matches'),
    url(r'^$', league, name='league'),
]
