import csv
from datetime import datetime
from django.utils import timezone

import re
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from matches.models import Match, Bet, parse_score


class Command(BaseCommand):
    help = 'Load data from google docs'

    def add_arguments(self, parser):
        parser.add_argument('dump_file', nargs=1, type=open)

    def handle(self, *args, **options):
        call_command('flush','--noinput')
        self.stdout.write(self.style.WARNING('Successfully flushed data'))

        f = options['dump_file'][0]
        data = csv.reader(f)
        usernames = next(data)[3:-1]
        users = [User.objects.create(username=username) for username in usernames]
        for row in data:
            datetime_object = timezone.make_aware(datetime.strptime('2017'+row[0]+row[1], '%Y%d.%m%H:%M'))
            home_team, away_team = row[2].split(' — ')
            match = Match.objects.create(
                datetime = datetime_object,
                home_team = home_team,
                away_team = away_team
            )
            for user, bet in zip(users,row[3:-1]):
                bet_parsed = parse_score(bet)
                if bet_parsed:
                    home_score = bet_parsed[0]
                    away_score = bet_parsed[1]
                    bet_object = Bet(
                        match_id = match.id,
                        user=user,
                        home_score=home_score,
                        away_score=away_score
                    )
                    bet_object.save()

            result = row[-1]
            result_parsed = parse_score(result)
            if result_parsed:
                match.set_score(*result_parsed)

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))