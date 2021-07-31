from django.test import TestCase
from .forms import RegisterForm

# Create your tests here.
class ViewsTestCase(TestCase):
    def test_register_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('http://localhost:8000/register/')
        self.assertEqual(response.status_code, 200)


class FormsTestCase(TestCase):
    def test_register_loads_properly(self):
        form = RegisterForm(data={
            'email': 'j.doe@exemple.fr',
            'username': 'jdoe',
            'password1': 'qwertyuiop',
            'password2': 'qwertyuiop'
        })
        self.assertTrue(form.is_valid())