from django.urls import reverse

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTest


class UsersTest(FunctionalTest):
    def test_unauthenticated_can_login(self):
        self.user = UserFactory.create(username='ugo')
        self.password = self.user.password
        self.user.set_password(self.user.password)
        self.user.save()

        # Ugo goes to main page
        self.browser.get(self.live_server_url)
        # and see login button.
        login_link = self.browser.find_element_by_link_text('Login')
        # He clicks on it
        login_link.click()
        # and now he sees login form.
        self.wait_for(
            lambda: self.browser.find_element_by_id('id_username')
        )
        # He fills his credentials
        self.browser.find_element_by_id('id_username').send_keys(self.user.username)
        self.browser.find_element_by_id('id_password').send_keys(self.password)
        # and presses the only button
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        # and now he is redirected back to main page.
        # Now he sees logout button.
        self.wait_to_be_logged_in()
        # and logged in as text
        self.assertEqual(self.browser.find_element_by_css_selector('nav .navbar-text').text,
                         f'Logged in as ugo')

    def test_authenticated_can_change_password(self):
        # Ugo is logged-is user
        user = self.create_pre_authenticated_session('ugo')
        # Ugo goes to password change page
        self.browser.get(self.live_server_url+reverse('password_change'))
        # Ugo fill old password, and new one
        self.browser.find_element_by_id('id_old_password').send_keys('ugo666')
        self.browser.find_element_by_id('id_new_password1').send_keys('QAZwsx123')
        self.browser.find_element_by_id('id_new_password2').send_keys('QAZwsx123')
        # Press save button
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        # Now he redirected to main page
        self.wait_for(lambda : self.assertIn('/', self.browser.current_url))
        # Ugo loges out
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out()
        # Ugo goes to login page
        self.browser.get(self.live_server_url+reverse('login'))
        # and can login with new password
        self.browser.find_element_by_id('id_username').send_keys('ugo')
        self.browser.find_element_by_id('id_password').send_keys('QAZwsx123')
        self.browser.find_element_by_css_selector('input[type="submit"]').click()
        self.wait_to_be_logged_in()