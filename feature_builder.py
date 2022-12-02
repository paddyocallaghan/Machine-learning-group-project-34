from datetime import datetime
import pandas as pd
import helper_funcs
import previous_tables


def get_features(season_data, subset, raw_data, num_games=5):
    features = pd.DataFrame()
    for i in list(raw_data.keys())[1:]:
        for j, r in raw_data[i].iterrows():
            home_team = r['HomeTeam']
            away_team = r['AwayTeam']
            try:
                match_date = datetime.strptime(r['Date'], '%d/%m/%y')
            except:
                match_date = datetime.strptime(r['Date'], '%d/%m/%Y')


            home_match_count = \
                subset[i][home_team].query('ground == "H" and TeamAgainst =="' + away_team + '"')['match'].values[0]
            away_team_match_count =\
                subset[i][away_team].query('ground == "A" and TeamAgainst =="' + home_team + '"')['match'].values[0]


            if home_match_count > 1:
                home_team_last_game = subset[i][home_team].loc[home_match_count - 1,]
            else:
                home_team_last_game = 0

            if away_team_match_count > 1:
                away_team_last_game = subset[i][home_team].loc[away_team_match_count - 1,]
            else:
                away_team_last_game = 0


            #Home team
            home_team_prev_games = subset[i][home_team].loc[home_match_count - num_games:home_match_count - 1, ]
            home_team_prev_home_games = subset[i][home_team].query('ground == "H"')
            home_team_num_home_games = list(home_team_prev_home_games.index).index(home_match_count)
            home_team_prev_home_games = \
                home_team_prev_home_games.iloc[home_team_num_home_games - num_games:home_team_num_home_games, ]

            if home_team in season_data[i - 1]['Team']:
                hs_prev_season_sum = season_data[i - 1].loc[season_data[i - 1]['Team'] == home_team]
            else:
                #if no previous season use average = 10th
                hs_prev_season_sum = season_data[i - 1].loc[season_data[i - 1]['Position'] == 10]
            try:
                hs_prev_season = subset[i - 1][home_team]
            except:
                hs_prev_season = subset[i - 1][season_data[i - 1].iloc[10,]['home_Team']]

            #get last season home vs away team
            home_vs_away_prev_season = hs_prev_season.query('TeamAgainst =="' + away_team + '"')
            if not len(home_vs_away_prev_season):
                home_vs_away_prev_season = hs_prev_season.query(
                    'TeamAgainst =="' + season_data[i - 1].iloc[10,]['home_Team'] + '"')
            if not len(home_vs_away_prev_season):
                home_vs_away_prev_season = hs_prev_season.query(
                    'TeamAgainst =="' + season_data[i - 1].iloc[11,]['home_Team'] + '"')
            home_vs_away = subset[i][home_team].query(
                'match <' + str(home_match_count) + ' and TeamAgainst == "' + str(away_team) + '"')
            home_vs_away = home_vs_away_prev_season.append(home_vs_away)


            # Away team
            away_team_prev_games = subset[i][away_team].loc[away_team_match_count - num_games:away_team_match_count - 1, ]
            away_team_prev_away_games = subset[i][away_team].query('ground == "A"')
            away_team_num_away_games = list(away_team_prev_away_games.index).index(away_team_match_count)
            away_team_prev_away_games = away_team_prev_away_games.iloc[away_team_num_away_games - num_games:away_team_num_away_games, ]


            if away_team in season_data[i - 1]['Team']:
                as_prev_season_sum = season_data[i - 1].loc[season_data[i - 1]['Team'] == away_team]
            else:
                #if no previous season use average = 10th
                as_prev_season_sum = season_data[i - 1].loc[season_data[i - 1]['Position'] == 10]
            try:
                as_prev_season = subset[i - 1][away_team]
            except:
                as_prev_season = subset[i - 1][season_data[i - 1].iloc[10,]['home_Team']]

            #get away vs home last season
            away_vs_home_prev_season = as_prev_season.query('TeamAgainst =="' + home_team + '"')
            if not len(away_vs_home_prev_season):
                away_vs_home_prev_season = as_prev_season.query(
                    'TeamAgainst =="' + season_data[i - 1].iloc[10,]['home_Team'] + '"')
            if not len(away_vs_home_prev_season):
                away_vs_home_prev_season = as_prev_season.query(
                    'TeamAgainst =="' + season_data[i - 1].iloc[11,]['home_Team'] + '"')
            away_vs_home = subset[i][away_team].query('match <' + str(away_team_match_count) + ' and TeamAgainst == "' + str(home_team) + '"')
            away_vs_home = away_vs_home_prev_season.append(away_vs_home)

            features = features.append(
                pd.DataFrame({**previous_tables.prev_game_features(home_team_last_game, 'home', match_date),
                              **previous_tables.prev_game_features(away_team_last_game, 'away', match_date),
                              **previous_tables.prev_games_stats(home_team_prev_games, 'any', num_games),
                              **previous_tables.prev_games_stats(home_team_prev_home_games, 'home', num_games),
                              **previous_tables.prev_games_stats(away_team_prev_games, 'any', num_games),
                              **previous_tables.prev_games_stats(away_team_prev_away_games, 'away', num_games),
                              **previous_tables.prev_season_stats(hs_prev_season_sum, 'home'),
                              **previous_tables.prev_season_stats(as_prev_season_sum, 'away'),
                              **previous_tables.prev_vs_stats(home_vs_away, away_vs_home),
                              **helper_funcs.get_results(r)
                              }, index=[j, ]))
    return features
