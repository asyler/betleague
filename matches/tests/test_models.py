from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.factories import UserFactory
from matches.factories import PastMatchFactory, FutureMatchFactory
from matches.models import Match, Bet


class MatchModelTest(TestCase):
    def test_cant_be_without_fields(self):
        match = Match()
        with self.assertRaises(ValidationError):
            match.full_clean()

    def test_has_is_in_future_attr(self):
        past_match = PastMatchFactory.create()
        future_match = FutureMatchFactory.create()

        self.assertTrue(future_match.in_future)
        self.assertFalse(past_match.in_future)

class BetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.past_match = PastMatchFactory.create()
        cls.future_match = FutureMatchFactory.create()
        cls.user = UserFactory.create()

    def test_invalid_incorrect_score(self):
        bet = Bet(home_score='two', away_score=1, match=self.future_match, user=self.user)
        with self.assertRaises(ValidationError):
            bet.full_clean()

    def test_valid_correct_score(self):
        bet = Bet(home_score=2, away_score=1, match=self.future_match, user=self.user)
        bet.full_clean()
        # should not raise

    def test_valid_for_future_matches(self):
        bet = Bet(home_score=2, away_score=1, match=self.future_match, user=self.user)
        bet.full_clean()
        # should not raise

    def test_invalid_for_past_matches(self):
        bet = Bet(home_score=2, away_score=1, match=self.past_match, user=self.user)
        with self.assertRaises(ValidationError):
            bet.full_clean()

    def test_has_string_representation(self):
        bet = Bet(home_score=2, away_score=1, match=self.past_match, user=self.user)
        self.assertEqual(str(bet), '2 - 1')