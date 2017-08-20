from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import LoginForm


class LoginViewTest(TestCase):
    def try_auth(self,correct_login=True,correct_password=True):
        self.user = User.objects.create_user(username='ugo',password='ugo666')
        login = 'ugo' if correct_login else 'user_not_exist'
        password = 'ugo666' if correct_password else 'wrong_password'


        self.response = self.client.post('/accounts/login',
                                    data={
                                        'username': login,
                                        'password': password
                                    })

    def test_loads_login_form_on_GET(self):
        self.response = self.client.get('/accounts/login')
        self.assertIs(self.response.context['form'], LoginForm)

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

    def test_redirects_to_login_page_if_wrong_pass(self):
        self.try_auth(correct_login=False)
        self.assertRedirects(self.response, '/accounts/login')

    def test_redirects_to_login_page_if_not_exist(self):
        self.try_auth(correct_password=False)
        self.assertRedirects(self.response, '/accounts/login')