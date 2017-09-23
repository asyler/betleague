from django.contrib.auth.models import User
from django.db.models import Sum, Count, Case, When, IntegerField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from matches.models import Match, Bet


def matches(request):
    matches = Match.objects.all()
    users = User.objects.annotate(total_points=Coalesce(Sum('bet__result'),0)).order_by('pk').all()
    bets = Bet.objects.all().select_related('match')

    matches_array = {}
    for match in matches:
        match.bets = {}
        matches_array[match.pk] = match
    for bet in bets:
        matches_array[bet.match.pk].bets[bet.user.pk] = bet

    return render(request, 'matches.html', {
        'matches': matches_array,
        'users': users,
    })

def league(request):
    users = User.objects.annotate(
        points=Coalesce(Sum('bet__result'),0),
        matches_bet=Count('bet'),
        guess_hits=Count(Case(When(bet__result=12, then=1))
        )

    ).order_by('-points').all()

    return render(request, 'league.html', {
        'users': users
    })
