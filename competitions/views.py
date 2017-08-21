from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from matches.models import Match, Bet


def league(request):
    matches = Match.objects.all()
    users = User.objects.all()
    bets = Bet.objects.all().select_related('match')

    matches_array = {}
    for match in matches:
        match.bets = {}
        matches_array[match.pk] = match
    for bet in bets:
        matches_array[bet.match.pk].bets[bet.user.pk] = bet

    return render(request, 'league.html', {
        'matches': matches_array,
        'users': users,
    })