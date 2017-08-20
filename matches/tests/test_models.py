from django.core.exceptions import ValidationError
from django.test import TestCase

from matches.models import Match


class MatchModelTest(TestCase):
    def test_cant_be_without_fields(self):
        match = Match()
        with self.assertRaises(ValidationError):
            match.full_clean()