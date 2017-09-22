from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase

from accounts.factories import UserFactory



class LoginViewTest(TestCase):
    def try_auth(self, correct_login=True, correct_password=True):
        self.user = UserFactory.create()
        login = self.user.username if correct_login else 'user_not_exist'
        password = self.user.raw_password if correct_password else 'wrong_password'

        self.response = self.client.post('/accounts/login',
                                         data={
                                             'username': login,
                                             'password': password
                                         })

    def test_loads_login_form_on_GET(self):
        self.response = self.client.get('/accounts/login')
        self.assertIsInstance(self.response.context['form'], AuthenticationForm)

    def test_authenticate_user_if_exist(self):
        self.try_auth()
        self.assertIn('_auth_user_id', self.client.session)

    def test_not_authenticate_user_if_wrong_pass(self):
        self.try_auth(correct_password=False)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_not_authenticate_user_if_not_exist(self):
        self.try_auth(correct_login=False)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_redirects_to_home_page_if_success(self):
        self.try_auth()
        self.assertRedirects(self.response, '/')

    def test_returns_to_login_page_if_wrong_pass(self):
        self.try_auth(correct_login=False)
        self.assertEqual(self.response.status_code, 200)

    def test_returns_to_login_page_if_not_exist(self):
        self.try_auth(correct_password=False)
        self.assertEqual(self.response.status_code, 200)
