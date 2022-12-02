import os
import numpy as np
import pandas as pd

def getData(loc):
    df = pd.read_csv(loc, encoding='windows-1252', na_filter=True)
    colsToKeep = list(
        ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR", "HS", "AS", "HST",
         "AST", "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR"])
    allCols = df.columns
    colsToDrop = set(allCols) - set(colsToKeep)
    return df.drop(labels=colsToDrop, axis=1)


os.chdir("./dataset/Individual Data")

raw_data = {}
for i, j in enumerate(os.listdir()):
    raw_data[i] = getData(j)


def create_home_dict(table, index):
    match_dict = {}
    if any('FTR' == table.keys()):
        match_dict = {'Result': table['FTR'].values[0]}
    if any('FTHG' == table.keys()):
        match_dict.update({'Goals': table['FTHG'].values[0]})
    if any('FTAG' == table.keys()):
        match_dict.update({'GoalsAgainst': table['FTAG'].values[0]})
    match_dict.update({'match': index, 'ground': 'H',
                       'Date': table['Date'].values[0],
                       'TeamAgainst': table['AwayTeam'].values[0],
                       'HTGoals': table['HTHG'].values[0],
                       'HTResult': table['HTR'].values[0],
                       'Shots': table['HS'].values[0],
                       'ShotsAgainst': table['AS'].values[0],
                       'ShotsOnTarget': table['HST'].values[0],
                       'ShotsAgainstOnTarget': table['AST'].values[0],
                       'Corners': table['HC'].values[0],
                       'CornersAgainst': table['AC'].values[0],
                       'Fouls': table['HF'].values[0],
                       'FoulsAgainst': table['AF'].values[0],
                       'YCards': table['HY'].values[0],
                       'YCardsAgainst': table['AY'].values[0],
                       'RCards': table['HR'].values[0],
                       'RCardsAgainst': table['AR'].values[0]})
    if match_dict['Result'] == 'H':
        match_dict.update({'Win': 1, 'Draw': 0, 'Loss': 0})
    elif match_dict['Result'] == 'A':
        match_dict.update({'Win': 0, 'Draw': 0, 'Loss': 1})
    else:
        match_dict.update({'Win': 0, 'Draw': 1, 'Loss': 0})
    return pd.DataFrame(match_dict, index=[index, ])


def create_away_dict(table, index):
    match_dict = {}
    if any('FTR' == table.keys()):
        match_dict = {'Result': table['FTR'].values[0]}
    elif any('Res' == table.keys()):
        match_dict = {'Result': table['Res'].values[0]}
    if any('FTHG' == table.keys()):
        match_dict.update({'GoalsAgainst': table['FTHG'].values[0]})
    elif any('HG' == table.keys()):
        match_dict.update({'GoalsAgainst': table['HG'].values[0]})
    if any('FTAG' == table.keys()):
        match_dict.update({'Goals': table['FTAG'].values[0]})
    elif any('AG' == table.keys()):
        match_dict.update({'Goals': table['AG'].values[0]})
    match_dict.update({'match': index, 'ground': 'A',
                       'Date': table['Date'].values[0],
                       'TeamAgainst': table['HomeTeam'].values[0],
                       'HTGoals': table['HTAG'].values[0],
                       'HTResult': table['HTR'].values[0],
                       'Shots': table['AS'].values[0],
                       'ShotsAgainst': table['HS'].values[0],
                       'ShotsOnTarget': table['AST'].values[0],
                       'ShotsAgainstOnTarget': table['HST'].values[0],
                       'Corners': table['AC'].values[0],
                       'CornersAgainst': table['HC'].values[0],
                       'Fouls': table['AF'].values[0],
                       'FoulsAgainst': table['HF'].values[0],
                       'YCards': table['AY'].values[0],
                       'YCardsAgainst': table['HY'].values[0],
                       'RCards': table['AR'].values[0],
                       'RCardsAgainst': table['HR'].values[0]})
    if match_dict['Result'] == 'A':
        match_dict.update({'Win': 1, 'Draw': 0, 'Loss': 0})
    elif match_dict['Result'] == 'H':
        match_dict.update({'Win': 0, 'Draw': 0, 'Loss': 1})
    else:
        match_dict.update({'Win': 0, 'Draw': 1, 'Loss': 0})
    return pd.DataFrame(match_dict, index=[index, ])


def get_subset(team_data, subset):
    for i in team_data.keys():
        subset[i] = {}
        for j in list(set(team_data[i]['AwayTeam'])):
            subset[i][j] = pd.DataFrame()
            Table = team_data[i][(team_data[i]['AwayTeam'] == j) | (team_data[i]['HomeTeam'] == j)]
            for k in range(len(Table)):
                if j == Table.iloc[k]['AwayTeam']:
                    subset[i][j] = subset[i][j].append(create_away_dict(Table[k:k + 1], k + 1))
                elif j == Table.iloc[k]['HomeTeam']:
                    subset[i][j] = subset[i][j].append(create_home_dict(Table[k:k + 1], k + 1))
    return subset


def get_season_table(subset):
    table = {}
    for i in subset.keys():
        table[i] = pd.DataFrame()
        for j in subset[i].keys():
            table[i] = table[i].append(get_team_stats(subset[i][j], j))
        table[i] = table[i].sort_values(by=['Points', 'GD'], ascending=False)
        table[i]['Position'] = np.linspace(1, 20, 20)
    return table


def get_team_stats(team_team_data, team):
    home = team_team_data.query('ground == "H" ')
    away = team_team_data.query('ground == "A" ')

    season_dict = get_season_average(team_team_data, team)
    home_dict = get_season_average(home, team)
    away_dict = get_season_average(away, team)

    home_dict = dict(zip(["home_" + i for i in home_dict.keys()], home_dict.values()))
    away_dict = dict(zip(["away_" + i for i in away_dict.keys()], away_dict.values()))

    season_dict = {**season_dict, **home_dict, **away_dict}
    season_dict = {**season_dict, **{'Points': 3 * season_dict['Wins'] + (1 * season_dict['Draws']),
                                     'GD': season_dict['Goals'] - season_dict['GoalsAgainst']}}

    return pd.DataFrame(season_dict, index=[team, ])


def get_season_average(team_team_data, team):
    return {'Team': team,
            'Wins': sum(team_team_data['Win']),
            'Losses': sum(team_team_data['Loss']),
            'Draws': sum(team_team_data['Draw']),
            'Goals': sum(team_team_data['Goals']),
            'GoalsAgainst': sum(team_team_data['GoalsAgainst']),
            'YCards': sum(team_team_data['YCards']),
            'RCards': sum(team_team_data['RCards']),
            'avg_Goals': np.mean(team_team_data['Goals']),
            'avg_GoalsAgainst': np.mean(team_team_data['GoalsAgainst']),
            'avg_Corners': np.mean(team_team_data['Corners']),
            'avg_CornersAgainst': np.mean(team_team_data['CornersAgainst']),
            'avg_Fouls': np.mean(team_team_data['Fouls']),
            'avg_FoulsAgainst': np.mean(team_team_data['FoulsAgainst']),
            'avg_Shots': np.mean(team_team_data['Shots']),
            'avg_ShotsAgainst': np.mean(team_team_data['ShotsAgainst']),
            }


def get_results(team_data):
    match_dict = {}
    if any('FTR' == team_data.keys()):
        match_dict = {'Result': team_data['FTR']}
    elif any('Res' == team_data.keys()):
        match_dict = {'Result': team_data['Res']}
    if match_dict['Result'] == 'H':
        match_dict.update({'Win': 1, 'Draw': 0, 'Loss': 0})
    elif match_dict['Result'] == 'A':
        match_dict.update({'Win': 0, 'Draw': 0, 'Loss': 1})
    else:
        match_dict.update({'Win': 0, 'Draw': 1, 'Loss': 0})
    return match_dict
