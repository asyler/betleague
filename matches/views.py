from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.shortcuts import render, redirect

# Create your views here.
from matches.models import Match, Bet


@login_required
def user_bets(request):
    if request.method == 'POST':
        for match, result in request.POST.items():
            match_id = int(match[len('match_'):])
            bet = Bet.objects.filter(user=request.user, match__id=match_id).first()
            bet.set_bet(result)
            bet.save()
        return redirect('user_bets')

    matches = Match.objects.filter(Q(bet__user=request.user.pk) | Q(bet__user=None)).all()\
        .annotate(bet_home_score=F('bet__home_score'), bet_away_score=F('bet__away_score'))
    for match in matches:
        match.bet = Bet(match=match, user=request.user, home_score=match.bet_home_score, away_score=match.bet_away_score)
    return render(request, 'user_bets.html', {
        'matches': matches
    })
