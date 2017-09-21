from django.conf.urls import url
from django.contrib.auth.views import logout, PasswordChangeView, PasswordChangeDoneView

from . import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^password_change', PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change_done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]
