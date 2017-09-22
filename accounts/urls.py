from django.conf.urls import url
from django.contrib.auth.views import logout, PasswordChangeView, PasswordChangeDoneView, LoginView

from . import views

urlpatterns = [
    url(r'^login', LoginView.as_view(
        template_name='login.html'
    ), name='login'),
    url(r'^password_change', PasswordChangeView.as_view(
        template_name='password_change_form.html',
        success_url='/'
    ), name='password_change'),
    url(r'^password_change_done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]
