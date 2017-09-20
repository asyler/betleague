import datetime as datetime
import factory
from django.utils import timezone

from matches.models import Match, Bet


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Match

    home_team = factory.Faker('company')
    away_team = factory.Faker('company')


class PastMatchFactory(MatchFactory):
    datetime = timezone.now() - timezone.timedelta(days=1)

    home_score = factory.Faker('pyint')
    away_score = factory.Faker('pyint')


class FutureMatchFactory(MatchFactory):
    datetime = timezone.now() + timezone.timedelta(days=1)


class BetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bet

    home_score = factory.Faker('pyint')
    away_score = factory.Faker('pyint')