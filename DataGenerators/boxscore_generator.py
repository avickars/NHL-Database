import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import numpy as np
import datetime
from DataGenerators.players_generator import *
from mysql.connector.errors import Error


def get_boxscore():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'get_boxscore' order by date desc limit 1",
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
    games = pd.read_sql_query(f"select gameID from schedules where gameDate >= '{mostRecentRun}'", connection)

    for index, gameID in games.iterrows():
        print(gameID)
        gameID = gameID.values[0]

        url_string = f"https://statsapi.web.nhl.com/api/v1/game/{gameID}/feed/live"
        url = requests.get(url_string)
        url_data = url.json()

        # Getting player Stats
        for team in ['away', 'home']:
            try:
                teamID = url_data['liveData']['boxscore']['teams'][team]['team']['id']
            except KeyError:
                teamID = 'NULL'

            # Getting players who played
            players = url_data['liveData']['boxscore']['teams'][team]['players']
            for player in players:
                playerID = players[player]['person']['id']
                try:
                    jerseyNumber = players[player]['jerseyNumber']
                    if jerseyNumber == "":
                        jerseyNumber = 'NULL'
                except KeyError:
                    jerseyNumber = 'NULL'

                if players[player]['position']['code'] == 'G':
                    timeOnIce = f"\"{players[player]['stats']['goalieStats']['timeOnIce']}\""
                    plusMinus = 'NULL'
                    evenTimeOnIce = 'NULL'
                    powerPlayTimeOnIce = 'NULL'
                    shortHandedTimeOnIce = 'NULL'
                else:
                    try:
                        timeOnIce = f"\"{players[player]['stats']['skaterStats']['timeOnIce']}\""
                    except KeyError:
                        timeOnIce = 'NULL'

                    try:
                        plusMinus = players[player]['stats']['skaterStats']['plusMinus']
                    except KeyError:
                        plusMinus = 'NULL'

                    try:
                        evenTimeOnIce = f"\"{players[player]['stats']['skaterStats']['evenTimeOnIce']}\""
                    except KeyError:
                        evenTimeOnIce = 'NULL'

                    try:
                        powerPlayTimeOnIce = f"\"{players[player]['stats']['skaterStats']['powerPlayTimeOnIce']}\""
                    except KeyError:
                        powerPlayTimeOnIce = 'NULL'

                    try:
                        shortHandedTimeOnIce = f"\"{players[player]['stats']['skaterStats']['shortHandedTimeOnIce']}\""
                    except KeyError:
                        shortHandedTimeOnIce = 'NULL'
                if timeOnIce != 'NULL':
                    unknown = 0
                    scratched = 0
                    if timeOnIce == "\"0:00\"":
                        unknown = 1
                else:
                    unknown = 1
                    scratched = 'NULL'

                query = f"insert into box_scores values (" \
                        f"{gameID}," \
                        f"{teamID}," \
                        f"{playerID}," \
                        f"{jerseyNumber}," \
                        f"{timeOnIce}," \
                        f"{plusMinus}," \
                        f"{evenTimeOnIce}," \
                        f"{powerPlayTimeOnIce}," \
                        f"{shortHandedTimeOnIce}," \
                        f"{unknown}," \
                        f"{scratched})"
                try:
                    cursor.execute(query)
                    connection.commit()
                except Error:
                    print("ERROR")
                    print(query)
                    return -1

            scratches = url_data['liveData']['boxscore']['teams'][team]['scratches']
            for playerID in scratches:
                playerAlreadyIn = pd.read_sql_query(f"select * from box_scores where playerID = {playerID} and gameID = {gameID} and teamID = {teamID}",
                                                  connection)
                if len(playerAlreadyIn) == 0:
                    timeOnIce = 'NULL'
                    plusMinus = 'NULL'
                    evenTimeOnIce = 'NULL'
                    powerPlayTimeOnIce = 'NULL'
                    shortHandedTimeOnIce = 'NULL'
                    scratched = 1
                    unknown = 'NULL'

                    query = f"insert into box_scores values (" \
                            f"{gameID}," \
                            f"{teamID}," \
                            f"{playerID}," \
                            f"{jerseyNumber}," \
                            f"{timeOnIce}," \
                            f"{plusMinus}," \
                            f"{evenTimeOnIce}," \
                            f"{powerPlayTimeOnIce}," \
                            f"{shortHandedTimeOnIce}," \
                            f"{unknown}," \
                            f"{scratched})"
                else:
                    query = f"update box_scores set unknown = 0, scratched=1 where playerID = {playerID} and teamID = {teamID} and gameID = {gameID}"

                try:
                    cursor.execute(query)
                    connection.commit()
                except Error:
                    print("ERROR")
                    print(query)
                    return -1


    conn.close()
