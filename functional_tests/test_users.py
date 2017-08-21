from django.contrib.auth.models import User

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTest


class UsersTest(FunctionalTest):
    def setUp(self):
        self.user = UserFactory.create()
        self.password = self.user.password
        self.user.set_password(self.user.password)
        self.user.save()
        super().setUp()

    def test_unauthenticated_can_login(self):
        # Ugo goes to main page
        self.browser.get(self.live_server_url)
        # and see login button.
        login_link = self.browser.find_element_by_link_text('Login')
        # He clicks on it
        login_link.click()
        # and now he sees login form.
        self.wait_for(
            lambda : self.browser.find_element_by_id('id_username')
        )
        # He fills his credentials
        self.browser.find_element_by_id('id_username').send_keys(self.user.username)
        self.browser.find_element_by_id('id_password').send_keys(self.password)
        # and presses the only button
        self.browser.find_element_by_tag_name('button').click()
        # and now he is redirected back to main page.
        # Now he sees logout button.
        self.wait_to_be_logged_in()
