from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import datetime
import pandas as pd
import numpy as np


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'predict_wins' order by date desc limit 1",
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

    # Getting all the games that we can bet on
    schedule = pd.read_sql_query(f"""
                                     select gameID, 
                                             gameDate, 
                                             awayTeamID,
                                             homeTeamID 
                                     from schedules 
                                     where gameDate >= {mostRecentRun} and 
                                           seasonID >= 20112012 and
                                           gameType in (\'P\',\'R\')
                                           """, connection)

    predict_game_outcome(schedule)

    conn.close()


def predict_game_outcome(schedule):
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, 'stage_hockey', creds.user, creds.password)
    connection = conn.open()
    for index, game in schedule.iterrows():
        homeData = pd.read_sql_query(f"""
                                     select shotsForPerGame,
                                           goalsForPerGame,
                                           shotsAgainstPerGame,
                                           goalsAgainstPerGame,
                                           winningPercentage,
                                           shotDifferential,
                                           goalDifferential
                                    from stage_hockey.game_prediction_team_stats
                                    where teamID = {game['homeTeamID']} and
                                          gameDate < \'{game['gameDate']}\' and
                                          gameType = 'R'
                                    order by gameID desc
                                    limit 1
                                           """, connection)

        awayData = pd.read_sql_query(f"""
                                      select shotsForPerGame,
                                            goalsForPerGame,
                                            shotsAgainstPerGame,
                                            goalsAgainstPerGame,
                                            winningPercentage,
                                            shotDifferential,
                                            goalDifferential
                                     from stage_hockey.game_prediction_team_stats
                                     where teamID = {game['awayTeamID']} and
                                           gameDate < \'{game['gameDate']}\' and
                                           gameType = 'R'
                                     order by gameID desc
                                     limit 1
                                            """, connection)

        boxscores = pd.read_sql_query(f"""
                                        select teamID, playerID
                                        from boxscores 
                                        where gameID = {game['gameID']} and scratched = 0
                                        """, connection)

        print(game)

        break

    conn.close()


if __name__ == '__main__':
    main()
