from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
import datetime
import numpy as np
from DataGenerators.players_generator import get_player, get_other_player_info
from DataGenerators.get_time import get_time
from pickle import load
import pickle
import mysql.connector.errors as Errors


def get_game_outcome_predictions():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'get_game_outcome_predictions' order by date desc limit 1",
                                      connection)

    # If we've never run it before, we start from the beginning
    if len(mostRecentRun) == 0:
        date_time_str = '2000-10-04 01:55:19'
        mostRecentRun = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        mostRecentRun = mostRecentRun.date()
    else:
        # Otherwise just converting it into sql form
        # Converting it from np.datetime64 to datetime
        # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
        mostRecentRun = mostRecentRun.date()

    # Getting all the games we need to get the live data for (i.e. everything from our last run up to games played yesterday)
    minGameID = pd.read_sql_query(f"select min(gameID) from schedules where gameDate >= '{mostRecentRun}'", connection).values[0][0]

    if minGameID is None:
        return 0

    games = pd.read_sql_query(f"select * from schedules where gameID >= {minGameID} and gameDate < \'{datetime.date.today()}\'", connection)

    for index, game in games.iterrows():
        print(game['gameID'])
        # Getting players that are playing in the game
        boxscores = pd.read_sql_query(f"select teamID, playerID, scratched, gameID from box_scores where gameID = {game['gameID']} and timeOnIce is not null", connection)

        # Getting all players GIM values from their last game
        playerGIMS = []
        for index, player in boxscores.iterrows():
            cursor.execute(f"""
              select gimMeanAdjusted
                from stage_hockey.gim_values_consolidated
                where playerID = {player['playerID']} and
                        gameID < {game['gameID']}
                order by gameID desc
                limit 1
            """)
            indvGIM = cursor.fetchall()

            # If we have previous data on the player
            if len(indvGIM) > 0:
                playerGIMS.append([player['teamID'], indvGIM[0][0]])

            # If we have no previous data on the player (i.e. its their first NHL game)
            else:
                # If this is their first nhl game, we won't have them in the system, must fetch their data (we need their position to get the positional average GIM)

                # Testing if they are in the system
                cursor.execute(f"""
                                                           select * from players where playerID = {player['playerID']}
                                                         """)
                playerInfo = cursor.fetchall()

                # They aren't in the system
                if len(playerInfo) == 0:
                    get_player(connection, player['playerID'])
                    get_other_player_info(connection, player['playerID'], f"\'{get_time()}\'")

                cursor.execute(f"""
                       select gimMean
                        from stage_hockey.gim_position_averages_per_season
                        where seasonID = (select previousSeasonID
                                            from season_to_next_season_mapping
                                            where seasonID = (select max(seasonID) from seasons)) and
                              primaryPositionCode = (select primaryPositionCode
                                                    from plays_position
                                                    where playerID = {player['playerID']}
                                                    order by  date desc
                                                    limit 1)
                            """)
                try:
                    playerGIMS.append([player['teamID'], cursor.fetchall()[0][0]])
                except IndexError:
                    # This is here as a found in 1 case, the player had a playeriD but no more info (i.e. no position), so the above query returned nothing and through an index error
                    continue
        teamGIMValues = pd.DataFrame(playerGIMS, columns=['teamID', 'GIM_VALUE'])
        teamGIMValues = teamGIMValues.groupby(['teamID']).sum().reset_index()

        # Getting home team data
        gameTeamValues = [[]]
        for team in [game['homeTeamID'], game['awayTeamID']]:
            if game['gameType'] == 'R':
                cursor.execute(f"""
                            select shotsForPerGame,
                                   goalsForPerGame,
                                   shotsAgainstPerGame,
                                   goalsAgainstPerGame,
                                   winningPercentage,
                                   shotDifferential,
                                   goalDifferential,
                                   gameNumber
                            from stage_hockey.game_prediction_team_stats
                            where gameID < {game['gameID']} and
                                  teamID = {team} and
                                  gameType = 'R'
                            order by gameDate desc
                            limit 1
                             """)
            else:
                cursor.execute(f"""
                                select shotsForPerGame,
                                       goalsForPerGame,
                                       shotsAgainstPerGame,
                                       goalsAgainstPerGame,
                                       winningPercentage,
                                       shotDifferential,
                                       goalDifferential,
                                       gameNumber
                                from stage_hockey.game_prediction_team_stats
                                where gameID < {game['gameID']} and
                                      teamID = {team}
                                order by gameDate desc
                                limit 1
                                         """)
            teamValues = cursor.fetchall()
            if len(teamValues) == 0:
                cursor.execute(f"""
                                  select shotsForPerGame,
                                            goalsForPerGame,
                                            shotsAgainstPerGame,
                                            goalsAgainstPerGame,
                                            winningPercentage,
                                            shotDifferential,
                                            goalDifferential,
                                            1 as gameNumber
                                    from stage_hockey.team_stats_by_season
                                    where nextSeasonID = {game['seasonID']}
                                           """)
                teamValues = cursor.fetchall()

            for i in teamValues[0]:
                gameTeamValues[0].append(i)
        modelInput = pd.DataFrame(gameTeamValues, columns=['home_shotsForPerGame',
                                                           'home_goalsForPerGame',
                                                           'home_shotsAgainstPerGame',
                                                           'home_goalsAgainstPerGame',
                                                           'home_winningPercentage',
                                                           'home_shotDifferential',
                                                           'home_goalDifferential',
                                                           'home_gameNumber',
                                                           'away_shotsForPerGame',
                                                           'away_goalsForPerGame',
                                                           'away_shotsAgainstPerGame',
                                                           'away_goalsAgainstPerGame',
                                                           'away_winningPercentage',
                                                           'away_shotDifferential',
                                                           'away_goalDifferential',
                                                           'away_gameNumber'])
        modelInput['gameID'] = game['gameID']
        modelInput['homeTeamID'] = game['homeTeamID']
        modelInput['awayTeamID'] = game['awayTeamID']
        modelInput['home_GIM_VALUE'] = teamGIMValues[teamGIMValues['teamID'] == game['homeTeamID']]['GIM_VALUE'].values[0]
        modelInput['away_GIM_VALUE'] = teamGIMValues[teamGIMValues['teamID'] == game['awayTeamID']]['GIM_VALUE'].values[0]

        # Ensuring the columns are always consistent
        modelInput = modelInput[['gameID', 'homeTeamID', 'awayTeamID', 'home_shotsForPerGame', 'home_goalsForPerGame',
                                 'home_shotsAgainstPerGame', 'home_goalsAgainstPerGame',
                                 'home_winningPercentage', 'home_shotDifferential',
                                 'home_goalDifferential', 'home_gameNumber', 'home_GIM_VALUE', 'away_shotsForPerGame',
                                 'away_goalsForPerGame', 'away_shotsAgainstPerGame',
                                 'away_goalsAgainstPerGame', 'away_winningPercentage',
                                 'away_shotDifferential', 'away_goalDifferential', 'away_gameNumber',
                                 'away_GIM_VALUE']]

        # Loading the scaler
        scaler = load(open('ETL/game_out_prediction_scaler.pkl', 'rb'))

        # Scaling the data
        scaledData = scaler.transform(modelInput.drop(['gameID', 'homeTeamID', 'awayTeamID'], axis=1).values)

        model = pickle.load(open('ETL/game_outcome_prediction_svm.sav', 'rb'))

        preds = model.predict(scaledData)
        query = f"insert into stage_hockey.game_outcome_prediction values ({game['gameID']},{game['homeTeamID']},{game['awayTeamID']},{preds[0]})"
        cursor.execute(query)
    connection.commit()

    conn.close()
