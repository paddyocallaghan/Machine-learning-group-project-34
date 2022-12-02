from datetime import datetime
import numpy as np


def prev_game_identity(home_or_away):
    return {home_or_away + '_gamesPlayed': 0,
            home_or_away + '_daysRested': 90,
            home_or_away + '_prev_game_Corners': 0,
            home_or_away + '_prev_game_CornersAgainst': 0,
            home_or_away + '_prev_game_Draw': 0,
            home_or_away + '_prev_game_FoulsAgainst': 0,
            home_or_away + '_prev_game_Fouls': 0,
            home_or_away + '_prev_game_Goals': 0,
            home_or_away + '_prev_game_GoalsAgainst': 0,
            home_or_away + '_prev_game_Loss': 0,
            home_or_away + '_prev_game_RCards': 0,
            home_or_away + '_prev_game_RCardsAgainst': 0,
            home_or_away + '_prev_game_Shots': 0,
            home_or_away + '_prev_game_ShotsAgainst': 0,
            home_or_away + '_prev_game_ShotsAgainstOnTarget': 0,
            home_or_away + '_prev_game_ShotsOnTarget': 0,
            home_or_away + '_prev_game_Win': 0,
            home_or_away + '_prev_game_YCards': 0,
            home_or_away + '_prev_game_YCardsAgainst': 0}


def prev_game_features(prev_game, home_or_away, md):
    if type(prev_game) == type(0):
        return prev_game_identity(home_or_away)
    try:
        mp = datetime.strptime(prev_game['Date'], "%d/%m/%y")
    except:
        mp = datetime.strptime(prev_game['Date'], "%d/%m/%Y")
    return {
            home_or_away + '_gamesPlayed': prev_game['match'],
            home_or_away + '_daysRested': (md - mp).days,
            home_or_away + '_prev_game_Corners': prev_game['Corners'],
            home_or_away + '_prev_game_CornersAgainst': prev_game['CornersAgainst'],
            home_or_away + '_prev_game_Draw': prev_game['Draw'],
            home_or_away + '_prev_game_FoulsAgainst': prev_game['FoulsAgainst'],
            home_or_away + '_prev_game_Fouls': prev_game['Fouls'],
            home_or_away + '_prev_game_Goals': prev_game['Goals'],
            home_or_away + '_prev_game_GoalsAgainst': prev_game['GoalsAgainst'],
            home_or_away + '_prev_game_Loss': prev_game['Loss'],
            home_or_away + '_prev_game_RCards': prev_game['RCards'],
            home_or_away + '_prev_game_RCardsAgainst': prev_game['RCardsAgainst'],
            home_or_away + '_prev_game_Shots': prev_game['Shots'],
            home_or_away + '_prev_game_ShotsAgainst': prev_game['ShotsAgainst'],
            home_or_away + '_prev_game_ShotsAgainstOnTarget': prev_game['ShotsAgainstOnTarget'],
            home_or_away + '_prev_game_ShotsOnTarget': prev_game['ShotsOnTarget'],
            home_or_away + '_prev_game_Win': prev_game['Win'],
            home_or_away + '_prev_game_YCards': prev_game['YCards'],
            home_or_away + '_prev_game_YCardsAgainst': prev_game['YCardsAgainst']}


def prev_games_stats(prev_games, home_or_away, count):
    return {
        home_or_away + '_avgCorners': np.mean(prev_games['Corners']),
        home_or_away + '_avgPoints': ((3 * sum(prev_games['Win'])) + sum(prev_games['Draw'])) / count,
        home_or_away + '_avgYCards': np.mean(prev_games['YCards']),
        home_or_away + '_acgRCards': np.mean(prev_games['RCards']),
        home_or_away + '_avgGoals': np.mean(prev_games['Goals']),
        home_or_away + '_avgGoalsAgainst': np.mean(prev_games['GoalsAgainst']),
        home_or_away + '_numWins': sum(prev_games['Win']),
        home_or_away + '_numLosses': sum(prev_games['Loss']),
        home_or_away + '_numDraws': sum(prev_games['Draw'])
    }


def prev_season_stats(prev_season, home_or_away):
    return {
        home_or_away + '_season_' + 'Position': prev_season['Position'].values[0],
        home_or_away + '_season_' + 'Draws': prev_season['Draws'].values[0],
        home_or_away + '_season_' + 'Wins': prev_season['Wins'].values[0],
        home_or_away + '_season_' + 'Losses': prev_season['Losses'].values[0],
        home_or_away + '_season_' + 'GD': prev_season['GD'].values[0],
        home_or_away + '_season_' + 'Points': prev_season['Points'].values[0],
        home_or_away + '_season_' + 'RCards': prev_season['RCards'].values[0],
        home_or_away + '_season_' + 'YCards': prev_season['YCards'].values[0],
        home_or_away + '_season_' + 'avg_Corners': prev_season['avg_Corners'].values[0],
        home_or_away + '_season_' + 'avg_CornersAgainst': prev_season['avg_CornersAgainst'].values[0],
        home_or_away + '_season_' + 'avg_Fouls': prev_season['avg_Fouls'].values[0],
        home_or_away + '_season_' + 'avg_FoulsAgainst': prev_season['avg_FoulsAgainst'].values[0],
        home_or_away + '_season_' + 'avg_Goals': prev_season['avg_Goals'].values[0],
        home_or_away + '_season_' + 'avg_GoalsAgainst': prev_season['avg_GoalsAgainst'].values[0],
        home_or_away + '_season_' + 'avg_Shots': prev_season['avg_Shots'].values[0],
        home_or_away + '_season_' + 'avg_ShotsAgainst': prev_season['avg_ShotsAgainst'].values[0],
        home_or_away + '_season_' + 'Draws': prev_season[home_or_away + '_' + 'Draws'].values[0],
        home_or_away + '_season_' + 'Wins': prev_season[home_or_away + '_' + 'Wins'].values[0],
        home_or_away + '_season_' + 'Losses': prev_season[home_or_away + '_' + 'Losses'].values[0],
        home_or_away + '_season_' + 'RCards': prev_season[home_or_away + '_' + 'RCards'].values[0],
        home_or_away + '_season_' + 'YCards': prev_season[home_or_away + '_' + 'YCards'].values[0],
        home_or_away + '_season_' + 'avg_Corners': prev_season[home_or_away + '_' + 'avg_Corners'].values[0],
        home_or_away + '_season_' + 'avg_CornersAgainst':
            prev_season[home_or_away + '_' + 'avg_CornersAgainst'].values[0],
        home_or_away + '_season_' + 'avg_Fouls': prev_season[home_or_away + '_' + 'avg_Fouls'].values[0],
        home_or_away + '_season_' + 'avg_FoulsAgainst': prev_season[home_or_away + '_' + 'avg_FoulsAgainst'].values[
            0],
        home_or_away + '_season_' + 'avg_Goals': prev_season[home_or_away + '_' + 'avg_Goals'].values[0],
        home_or_away + '_season_' + 'avg_GoalsAgainst': prev_season[home_or_away + '_' + 'avg_GoalsAgainst'].values[
            0],
        home_or_away + '_season_' + 'avg_Shots': prev_season[home_or_away + '_' + 'avg_Shots'].values[0],
        home_or_away + '_season_' + 'avg_ShotsAgainst': prev_season[home_or_away + '_' + 'avg_ShotsAgainst'].values[
            0],
    }


def prev_vs_stats(prev_games_h, prev_games_a):
    try:
        return {'hs_prev_vs_away_Win': prev_games_h['Win'].values[0],
                'hs_prev_vs_away_Loss': prev_games_h['Loss'].values[0],
                'hs_prev_vs_away_Draw': prev_games_h['Draw'].values[0],
                'hs_prev_vs_away_Goals': prev_games_h['Goals'].values[0],
                'hs_vs_away_avgCorners': np.mean(prev_games_h['Corners'].values[0]),
                'hs_vs_away_avgYCards': np.mean(prev_games_h['YCards'].values[0]),
                'hs_vs_away_avgRCards': np.mean(prev_games_h['RCards'].values[0]),
                'hs_vs_away_avgGoals': np.mean(prev_games_h['Goals'].values[0]),
                'as_prev_vs_home_Goals': prev_games_a['Goals'].values[0],
                'as_vs_home_avgCorners': np.mean(prev_games_a['Corners'].values[0]),
                'as_vs_home_avgYCards': np.mean(prev_games_a['YCards'].values[0]),
                'as_vs_home_avgRCards': np.mean(prev_games_a['RCards'].values[0]),
                'as_vs_home_avgGoals': np.mean(prev_games_a['Goals'].values[0])
                }
    except IndexError:

        return {'hs_prev_vs_away_Win': [0],
                'hs_prev_vs_away_Loss': [0],
                'hs_prev_vs_away_Draw': [0],
                'hs_prev_vs_away_Goals': [0],
                'hs_vs_away_avgCorners': [0],
                'hs_vs_away_avgYCards': [0],
                'hs_vs_away_avgRCards': [0],
                'hs_vs_away_avgGoals': [0],
                'as_prev_vs_home_Goals': [0],
                'as_vs_home_avgCorners': [0],
                'as_vs_home_avgYCards': [0],
                'as_vs_home_avgRCards': [0],
                'as_vs_home_avgGoals': [0],
                }

