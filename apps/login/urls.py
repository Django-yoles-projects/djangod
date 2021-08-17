from .views import log_in
from django.urls import path

app_name="login"

urlpatterns = [
    path('', log_in, name="login"),
]
