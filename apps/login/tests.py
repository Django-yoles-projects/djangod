from django.contrib.auth import authenticate
from django.http import response
from django.test import TestCase
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import LoginForm

# Create your tests here.

class FormsTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'usertest',
            'password': 'Qwertyuiop12!',
            'is_active': True
        }
        self.user = User.objects.create_user(**self.credentials)
        self.form = LoginForm()
        
    def test_login_has_fields(self):
        self.assertIn("username", self.form.fields)
        self.assertIn("password", self.form.fields)

    def test_login_empty(self):
        self.assertInHTML(
            f'<input type="text" name="username" autofocus autocapitalize="none" autocomplete="username" maxlength="150" class="form-control" required id="id_username">',
            str(self.form)
        ) 
        self.assertInHTML(
            f'<input type="password" name="password" autocomplete="current-password" class="form-control" required id="id_password">',
            str(self.form)
        )
    
    def test_login_is_valid(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid()) 
        
        fake_user = {
            'username': 'fake_user',
            'password': 'does not exist'
        }
        form = LoginForm(data=fake_user)
        self.assertFalse(form.is_valid())



class ViewsTestCase(TestCase):
    pass
    def setUp(self):
        self.url = reverse('accounts:login')
        self.credentials = {
            'username': 'usertest',
            'password': 'Qwertyuiop12!',
            'is_active': True
        }
        self.user = User.objects.create_user(**self.credentials)
    
    def test_login_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="login/login.html")


    def test_login_invalid_post(self):
        fake_user = {
            'username': 'fake_user',
            'password': 'does not exist'
        }
        response = self.client.post(self.url, fake_user)
        form_error = response.context['form'].errors.get('__all__')[0]
        
        self.assertEqual(form_error, "Saisissez un nom d’utilisateur et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).")
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_login_valid_post(self):
        response = self.client.post(self.url, self.credentials)
        self.failUnlessEqual(response.status_code, 302)
        
        user = User.objects.get(username=self.credentials.get('username'))
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.pk)        
