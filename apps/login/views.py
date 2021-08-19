from django.contrib.auth import views
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm


class LoginUser(views.LoginView):
    template_name="login/login.html"
    authentication_form=LoginForm


def log_out(request, *args, **kwargs):
    auth_logout(request)
    return redirect('accounts:login')
