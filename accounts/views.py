from django.contrib import auth
from django.shortcuts import redirect, render

from accounts.forms import LoginForm


def login(request):
    form = LoginForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            auth.login(request, form.get_user())
            return redirect('/')
        else:
            return redirect('/accounts/login')

    return render(request, 'user_login.html', {
        'form': LoginForm
    })
