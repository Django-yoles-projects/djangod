from django.contrib import messages
from django.contrib.auth import authenticate, views
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import LoginForm

def log_in(request, *args, **kwargs):
    if request.method == "POST":
    
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Vos identifiants sont incorrects.')
    form = LoginForm()
    return render(request, "login/login.html", {"form":form})

def log_out(request, *args, **kwargs):
    auth_logout(request)
    return redirect('accounts:login')
