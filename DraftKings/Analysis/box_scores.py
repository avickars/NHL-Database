import pandas as pd
import requests


def parse_goalies(data):
    try:
        stats = data['stats']['goalieStats']
    except KeyError:
        stats = {}

    try:
        timeOnIce = stats['timeOnIce']
    except KeyError:
        timeOnIce = None

    try:
        assists = stats['assists']
    except KeyError:
        assists = None

    try:
        goals = stats['goals']
    except KeyError:
        goals = None

    try:
        pim = stats['pim']
    except KeyError:
        pim = None

    try:
        shots = stats['shots']
    except KeyError:
        shots = None

    try:
        saves = stats['saves']
    except KeyError:
        saves = None

    try:
        powerPlaySaves = stats['powerPlaySaves']
    except KeyError:
        powerPlaySaves = None

    try:
        shortHandedSaves = stats['shortHandedSaves']
    except KeyError:
        shortHandedSaves = None

    try:
        evenSaves = stats['evenSaves']
    except KeyError:
        evenSaves = None

    try:
        shortHandedShotsAgainst = stats['shortHandedShotsAgainst']
    except KeyError:
        shortHandedShotsAgainst = None

    try:
        evenShotsAgainst = stats['evenShotsAgainst']
    except KeyError:
        evenShotsAgainst = None

    try:
        powerPlayShotsAgainst = stats['powerPlayShotsAgainst']
    except KeyError:
        powerPlayShotsAgainst = None

    try:
        decision = stats['decision']
    except KeyError:
        decision = None

    try:
        savePercentage = stats['savePercentage']
    except KeyError:
        savePercentage = None

    try:
        evenStrengthSavePercentage = stats['evenStrengthSavePercentage']
    except KeyError:
        evenStrengthSavePercentage = None

    try:
        powerPlaySavePercentage = stats['powerPlaySavePercentage']
    except KeyError:
        powerPlaySavePercentage = None

    values = {
        'timeOnIce': timeOnIce,
        'assists': assists,
        'goals': goals,
        'pim': pim,
        'shots': shots,
        'saves': saves,
        'powerPlaySaves': powerPlaySaves,
        'shortHandedSaves': shortHandedSaves,
        'evenSaves': evenSaves,
        'shortHandedShotsAgainst': shortHandedShotsAgainst,
        'evenShotsAgainst': evenShotsAgainst,
        'powerPlayShotsAgainst': powerPlayShotsAgainst,
        'decision': decision,
        'savePercentage': savePercentage,
        'evenStrengthSavePercentage': evenStrengthSavePercentage,
        'powerPlaySavePercentage': powerPlaySavePercentage
    }
    return values


def parse_players(data):
    try:
        stats = data['stats']['skaterStats']
    except KeyError:
        stats = {}

    try:
        timeOnIce = stats['timeOnIce']
    except KeyError:
        timeOnIce = None

    try:
        assists = stats['assists']
    except KeyError:
        assists = None

    try:
        goals = stats['goals']
    except KeyError:
        goals = None

    try:
        shots = stats['shots']
    except KeyError:
        shots = None

    try:
        hits = stats['hits']
    except KeyError:
        hits = None

    try:
        powerPlayGoals = stats['powerPlayGoals']
    except KeyError:
        powerPlayGoals = None

    try:
        powerPlayAssists = stats['powerPlayAssists']
    except KeyError:
        powerPlayAssists = None

    try:
        penaltyMinutes = stats['penaltyMinutes']
    except KeyError:
        penaltyMinutes = None

    try:
        faceOffPct = stats['faceOffPct']
    except KeyError:
        faceOffPct = None

    try:
        faceOffWins = stats['faceOffWins']
    except KeyError:
        faceOffWins = None

    try:
        faceoffTaken = stats['faceoffTaken']
    except KeyError:
        faceoffTaken = None

    try:
        takeaways = stats['takeaways']
    except KeyError:
        takeaways = None

    try:
        giveaways = stats['giveaways']
    except KeyError:
        giveaways = None

    try:
        shortHandedGoals = stats['shortHandedGoals']
    except KeyError:
        shortHandedGoals = None

    try:
        shortHandedAssists = stats['shortHandedAssists']
    except KeyError:
        shortHandedAssists = None

    try:
        blocked = stats['blocked']
    except KeyError:
        blocked = None

    try:
        plusMinus = stats['plusMinus']
    except KeyError:
        plusMinus = None

    try:
        evenTimeOnIce = stats['evenTimeOnIce']
    except KeyError:
        evenTimeOnIce = None

    try:
        powerPlayTimeOnIce = stats['powerPlayTimeOnIce']
    except KeyError:
        powerPlayTimeOnIce = None

    try:
        shortHandedTimeOnIce = stats['shortHandedTimeOnIce']
    except KeyError:
        shortHandedTimeOnIce = None

    values = {
        'timeOnIce': timeOnIce,
        'assists': assists,
        'goals': goals,
        'shots': shots,
        'hits': hits,
        'powerPlayGoals': powerPlayGoals,
        'powerPlayAssists': powerPlayAssists,
        'penaltyMinutes': penaltyMinutes,
        'faceOffPct': faceOffPct,
        'faceOffWins': faceOffWins,
        'faceoffTaken': faceoffTaken,
        'takeaways': takeaways,
        'giveaways': giveaways,
        'shortHandedGoals': shortHandedGoals,
        'shortHandedAssists': shortHandedAssists,
        'blocked': blocked,
        'plusMinus': plusMinus,
        'evenTimeOnIce': evenTimeOnIce,
        'powerPlayTimeOnIce': powerPlayTimeOnIce,
        'shortHandedTimeOnIce': shortHandedTimeOnIce,
    }

    return values


def main():
    games = pd.read_csv('data/gameIDs.csv', index_col=0)

    players_data = []

    goalies_data = []

    for index, values in games.iterrows():
        print(values['gameID'])
        url_string = f"https://statsapi.web.nhl.com/api/v1/game/{values['gameID']}/feed/live"
        url = requests.get(url_string)
        url_data = url.json()

        for team in ['away', 'home']:
            team_data = url_data['liveData']['boxscore']['teams'][team]

            goalies = team_data['goalies']

            players = team_data['players']

            for player in players.keys():
                playerID = int(player[2:])

                if playerID in goalies:
                    values = parse_goalies(players[player])

                    goalies_data.append(values)
                else:
                    values = parse_players(players[player])

                    players_data.append(values)



    players_df = pd.DataFrame(players_data)
    goalies_df = pd.DataFrame(goalies_data)

    players_df.to_csv('data/players_boxscores.csv')
    goalies_df.to_csv('data/goalies_boxscores.csv')


if __name__ == '__main__':
    main()
