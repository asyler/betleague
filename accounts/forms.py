from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    pass