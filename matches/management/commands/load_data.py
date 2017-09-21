import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from matches.models import Match, Bet


class Command(BaseCommand):
    help = 'Load data from google docs'

    def add_arguments(self, parser):
        parser.add_argument('dump_file', nargs=1, type=open)

    def handle(self, *args, **options):
        f = options['dump_file'][0]
        data = csv.reader(f)
        usernames = next(data)[3:-1]
        users = [User(username=username) for username in usernames]
        for row in data:
            datetime_object = datetime.strptime('2017'+row[0]+row[1], '%Y%d.%m%H:%M')
            home_team, away_team = row[2].split(' — ')
            match = Match(
                datetime = datetime_object,
                home_team = home_team,
                away_team= away_team
            )
            for user, bet in zip(users,row[3:-1]):
                bet = Bet(match = match, user=user)
                bet.set_bet(bet)
        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))