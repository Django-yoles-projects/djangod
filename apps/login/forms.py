from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    
    username = UsernameField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'autofocus': True}))

    # def __init__(self, request=None, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        # request = kwargs.pop('request')
        # self.request = request
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = User
        fields = ['username', 'password']