from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.messages import get_messages


import django.core.mail

from .forms import RegisterForm

import random 
import re
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


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


class ViewsTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register:signup')
        username = f'jdoe{random.randint(0, 100)}'
        self.data = {
            'email': 'j.doe@exemple.fr',
            'username': username,
            'password1': 'qwertyuiop12!',
            'password2': 'qwertyuiop12!'
        }
    
    def test_register_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="register/register.html")
    
    def test_register_post(self):
        data = self.data
        self.assertEqual(User.objects.count(), 0)
        response = self.client.post(self.url, data)
        self.failUnlessEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        
    def test_verify_email(self):
        response = self.client.post(self.url, self.data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pour finaliser votre inscription, vous devez confirmer votre email.')

        user = get_user_model().objects.get(email=self.data.get('email'))
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        activate_link = r"\/activate\/{}\/([A-Za-z0-9:\-]+)\/".format(uidb64)
        email_content = django.core.mail.outbox[0].alternatives[0][0]
        match = re.search(activate_link, email_content)# You might want to use some other way to raise an error for this
        assert match.groups(), "Could not find the token in the email"
        token = match.group(1)
        url = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})

        # Activate account through email link
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Votre compte à été confirmé. Vous pouvez dès à présent vous connecter.')

        # Retry an used link
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 3)
        self.assertEqual(str(messages[2]), "Le lien de confirmation n'est pas valide, ce lien a peut être déjà été utilisé.")



