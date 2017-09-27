from unittest import skip

from selenium.common.exceptions import NoSuchElementException

from functional_tests.base import FunctionalTest


class AdminTest(FunctionalTest):
    fixtures = ['accounts/fixtures/users.json', 'matches/fixtures/data.json']

    @skip
    def test_admin_can_add_matches(self):
        # Alice goes to admin page.
        # She sees login form.
        # She provides her login credentials
        # and now sees admin dashboard.
        # She notices "Matches" link
        # and clicks it.
        # Now she sees "Add" button
        # She clicks it
        # and now cal fill match info fields.
        # Then she clicks save button
        # and new match appears in table.
        self.fail('TODO')

    def test_admin_see_in_nav_link_to_edit_matches(self):
        # vladomar is logged-in admin
        self.create_pre_authenticated_session('vladomar')
        # vladomar goes to main page
        self.browser.get(self.live_server_url)
        # and see link to edit matches
        self.wait_for(lambda: self.browser.find_element_by_link_text('Edit matches'))
        # he clicks it
        self.browser.find_element_by_link_text('Edit matches').click()
        # and browser goes to edit matches page
        self.wait_for(lambda: self.assertIn('admin/matches/match/', self.browser.current_url))

    def test_not_admin_does_not_see_in_nav_link_to_edit_matches(self):
        # db is logged-in user, but not admin
        self.create_pre_authenticated_session('db')
        # db goes to main page
        self.browser.get(self.live_server_url)
        # and see no link to edit matches
        self.wait_to_be_logged_in()
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_link_text('Edit matches')
