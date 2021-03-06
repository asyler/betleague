class MatchesPage(object):
    def __init__(self, test):
        self.test = test

    def get_table(self):
        return self.test.browser.find_element_by_id('results_table')

    def get_matches(self):
        return self.test.browser \
            .find_elements_by_css_selector('tr.match')

    def get_match_info(self, match, field):
        return match.find_element_by_class_name(field).text

    def get_users(self):
        return self.test.browser \
            .find_elements_by_css_selector('td.username')

    def get_user_username(self, user):
        return user.text

    def find_user_index(self, username):
        users = self.get_users()
        user = next((
            x for x in users if
            x.text == username
        ))
        user_index = users.index(user)
        return user_index

    def find_match(self, home_team, away_team):
        matches = self.get_matches()

        match = next((
            x for x in matches if
            self.get_match_info(x, 'home_team') == home_team and
            self.get_match_info(x, 'away_team') == away_team
        ))
        return match

    def _find_bet(self, home_team, away_team, username, class_name):
        match = self.find_match(home_team, away_team)

        user_index = self.find_user_index(username)
        bet = match.find_elements_by_class_name(class_name)[user_index]
        return bet

    def find_bet(self, home_team, away_team, username):
        return self._find_bet(home_team, away_team, username, 'bet')

    def find_bet_result(self, home_team, away_team, username):
        return self._find_bet(home_team, away_team, username, 'bet_result')

    def get_total_row(self):
        return self.test.browser.find_element_by_css_selector('tr#total')

    def get_total(self, username):
        user_index = self.find_user_index(username)
        total_row = self.get_total_row()
        return total_row.find_elements_by_css_selector('td.points')[user_index].text

    def get_bet_points_switcher(self):
        return self.test.browser.find_element_by_css_selector('#bet_points_switcher')

    def switcher_is_on(self):
        return 'off' not in self.test.browser.find_element_by_css_selector('.toggle.btn').get_attribute('class')

    def switcher_click(self):
        self.test.browser.find_element_by_css_selector('.toggle.btn').click()

    def get_result_element(self, home_team, away_team):
        match = self.find_match(home_team, away_team)
        return match.find_element_by_class_name('result')

    def get_result(self, home_team, away_team):
        return self.get_result_element(home_team,away_team).text


