from django.urls import reverse
from selenium.webdriver.common.by import By


class LeaguePage(object):
    def __init__(self, test):
        self.test = test

        self.url = self.test.live_server_url + reverse('league')

    def go(self):
        self.test.browser.get(self.url)

    def find_user_row(self, username):
        return self.test.browser.find_element(By.XPATH, f'//td[@class="username"][text()="{username}"]/..')

    def find_user(self, username):
        return self.test.browser.find_element(By.XPATH, f'//td[@class="username"][text()="{username}"]')

    def find_user_info(self, username, css_class):
        username_el = self.find_user(username)
        return username_el.find_element(By.XPATH, f'.//following-sibling::td[@class="{css_class}"]')

    def find_user_matches_bet(self, username):
        return self.find_user_info(username, 'matches_bet').text

    def find_user_points(self, username):
        return self.find_user_info(username, 'points').text

    def find_user_12s(self, username):
        return self.find_user_info(username, 'guess_hits').text

