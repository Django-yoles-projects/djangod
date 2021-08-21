"""djangod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.register.views import ActivateAccount
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

import debug_toolbar

urlpatterns = [
    # path('', lambda request : render(request, 'core/home.html'), name="home"),
    path('', include('apps.blog.urls'), name="blog"),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.custom_auth.urls'), name="accounts"),
    path("register/", include('apps.register.urls'), name="register"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('__debug__/', include(debug_toolbar.urls)),
    # url(r'^__debug__/', include(debug_toolbar.urls)),
]
# SHOW_TOOLBAR_CALLBACK = True