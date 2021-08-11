from django.urls import path
from .views import home, register, verification

app_name="register"

urlpatterns = [
    path('', register, name="signup"),
    path('verification', verification, name="verification"),
]
