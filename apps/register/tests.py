from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import RegisterForm
import random 


class FormsTestCase(TestCase):
    def setUp(self):
        username = f'jdoe{random.randint(0, 100)}'
        self.form_data = {
            'email': 'j.doe@exemple.fr',
            'username': username,
            'password1': 'qwertyuiop12!',
            'password2': 'qwertyuiop12!'
        }
        self.form = RegisterForm(data=self.form_data)
        
    def test_register_has_fields(self):
        self.assertIn("email", self.form.fields)
        self.assertIn("username", self.form.fields)
        self.assertIn("password1", self.form.fields)
        self.assertIn("password2", self.form.fields)

    def test_register_empty(self):
        self.assertInHTML(
            f'<input type="text" name="username" value="{self.form_data.get("username")}" maxlength="150" class="form-control" required id="id_username">', str(self.form)
        ) 
        self.assertInHTML(
            f'<input type="email" name="email" value="{self.form_data.get("email")}" class="form-control" required id="id_email">', str(self.form)
        )
        self.assertInHTML(
            f'<input type="password" name="password1" autocomplete="new-password" class="form-control" required id="id_password1">', str(self.form)
        )
        self.assertInHTML(
            f'<input type="password" name="password2" autocomplete="new-password" class="form-control" required id="id_password2">', str(self.form)
        )
    
    def test_register_is_valid(self):
        request = HttpRequest()
        request.POST = self.form_data
        form = RegisterForm(request.POST)
        self.assertTrue(form.is_valid())
    

    def test_register_is_user_created(self):
        request = HttpRequest()
        request.POST = self.form_data
        form = RegisterForm(request.POST)
        self.assertEqual(User.objects.count(), 0)
        form.save()
        self.assertEqual(User.objects.count(), 1)

    
# Create your tests here.
class ViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.url = reverse('register:signup')
    
    def test_register_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="register/register.html")
    
    def test_register_post(self):
        username = f'jdoe{random.randint(0, 100)}'
        data = {
            'email': 'j.doe@exemple.fr',
            'username': username,
            'password1': 'qwertyuiop12!',
            'password2': 'qwertyuiop12!'
        }
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(self.url, data)
        self.failUnlessEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        

