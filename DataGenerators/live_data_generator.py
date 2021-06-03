import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import numpy as np
import datetime
import pyodbc
from DataGenerators.players_generator import *


def get_live_data():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select top 1 date from script_execution where script = 'get_live_data' order by date desc",
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

        for event in url_data['liveData']['plays']['allPlays']:

            playerID = []
            playerType = []
            try:
                for player in event['players']:
                    try:
                        playerID.append(player['player']['id'])
                    except IndexError:
                        playerID.append('NULL')
                    except KeyError:
                        playerID.append('NULL')

                    try:
                        playerType.append(player['playerType'])
                    except IndexError:
                        playerType.append('NULL')
                    except KeyError:
                        playerType.append('NULL')
            except KeyError:
                playerID.append('NULL')
                playerType.append('NULL')

            try:
                teamID = event['team']['id']
            except KeyError:
                teamID = 'NULL'

            try:
                gameEvent = f"\'{event['result']['event']}\'"
            except KeyError:
                gameEvent = 'NULL'

            try:
                eventCode = f"\'{event['result']['eventCode']}\'"
            except KeyError:
                eventCode = 'NULL'

            try:
                eventTypeID = f"\'{event['result']['eventTypeId']}\'"
            except KeyError:
                eventTypeID = 'NULLeventTypeID'

            try:
                eventDescription = f"{event['result']['description']}"
                eventDescription = eventDescription.replace("\'", " ")
                eventDescription = "\'" + eventDescription + "\'"
            except KeyError:
                eventDescription = 'NULL'
            try:
                secondaryType = f"{event['result']['secondaryType']}"
                secondaryType = secondaryType.replace("\'", " ")
                secondaryType = "\'" + secondaryType + "\'"
            except KeyError:
                secondaryType = 'NULL'

            try:
                periodNum = event['about']['period']
            except KeyError:
                periodNum = 'NULL'

            eventID = event['about']['eventId']

            try:
                periodTime = f"\'{event['about']['periodTime']}\'"
            except KeyError:
                periodTime = 'NULL'

            try:
                xCoordinate = event['coordinates']['x']
            except KeyError:
                xCoordinate = 'NULL'

            try:
                yCoordinate = event['coordinates']['y']
            except KeyError:
                yCoordinate = 'NULL'

            try:
                penaltySeverity = f"\'{event['result']['penaltySeverity']}\'"
            except KeyError:
                penaltySeverity = 'NULL'

            try:
                penaltyMinutes = event['result']['penaltyMinutes']
            except KeyError:
                penaltyMinutes = 'NULL'

            for i in range(0, len(playerID)):
                query = f"insert into live_feed values (" \
                        f"{eventID}," \
                        f"{i}," \
                        f"{gameID}," \
                        f"{gameEvent}," \
                        f"{eventCode}," \
                        f"{eventTypeID}," \
                        f"{eventDescription}," \
                        f"{secondaryType}," \
                        f"{periodNum}," \
                        f"{periodTime}," \
                        f"{playerID[i]}," \
                        f"\'{playerType[i]}\'," \
                        f"{xCoordinate}," \
                        f"{yCoordinate}," \
                        f"{teamID}," \
                        f"{penaltySeverity}," \
                        f"{penaltyMinutes})"
                try:
                    cursor.execute(query)
                    connection.commit()
                except pyodbc.ProgrammingError:
                    print(query)
                    return -1

    conn.close()
