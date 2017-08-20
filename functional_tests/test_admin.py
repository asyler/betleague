from functional_tests.base import FunctionalTest


class AdminTest(FunctionalTest):
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