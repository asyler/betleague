def calc_result(home, away):
    if home < away:
        return 'lose'
    elif home > away:
        return 'win'
    else:
        return 'draw'


def calc_bet_result(
        home_score, away_score,
        home_bet, away_bet,
        shootout_winner=None,
        shootout_bet=None,
):
    if home_score == home_bet and away_score == away_bet:
        score = 12
    elif home_score - away_score == home_bet - away_bet:
        score = 6
    else:
        score = 0

        match_result = calc_result(home_score, away_score)
        bet_result = calc_result(home_bet, away_bet)

        if match_result == bet_result:
            score += 3
        if home_score + away_score == home_bet + away_bet and home_score + away_score >= 4:
            score += 2
        if home_score == home_bet or away_score == away_bet:
            score += 2

    if shootout_winner is not None:
        if shootout_bet == shootout_winner:
            if score in (6, 12):
                # only in this cases you can guess penalty shootout
                score += 4

    return score if score > 0 else 1

# nothing   total1  total4  result  diff    all     shootout     |   score
# +                                                             |   1
#           +                                                   |   2
#                   +                                           |   2
#                           +                                   |   3
#           +               +                                   |   5
#                   +       +                                   |   5
#                                   +                           |   6
#                                           +                   |   12
#                                   +               +           |   6 + 4 = 10
#                                           +       +           |   12 + 4 = 16
