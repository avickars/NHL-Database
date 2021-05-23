import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import numpy as np
import datetime


def get_live_date():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select top 1 date from script_execution where script = 'get_live_date' order by date desc",
                                      connection)

    # If we've never run it before, we start from the beginning
    if len(mostRecentRun) == 0:
        date_time_str = '2000-10-04 01:55:19'
        mostRecentRun = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        mostRecentRun = mostRecentRun.date()
        print(mostRecentRun)
    else:
        # Otherwise just convering it into sql form
        # Converting it from np.datetime64 to datetime
        # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
        mostRecentRun = mostRecentRun.date()

    # Getting all the games we need to get the live data for (i.e. everything from our last run up to games played yesterday)
    games = pd.read_sql_query(f"select gameID from schedules where gameDate >= '{mostRecentRun}'", connection)

    for index, gameID in games.iterrows():
        gameID = gameID.values[0]
        url_string = f"https://statsapi.web.nhl.com/api/v1/game/{gameID}/feed/live"
        url = requests.get(url_string)
        url_data = url.json()

        for event in url_data['liveData']['plays']['allPlays']:
            try:
                playerTwoID = event['players'][1]['player']['id']
            except KeyError:
                playerTwoID = 'NULL'
            except IndexError:
                playerTwoID = 'NULL'

            try:
                playerOneID = event['players'][0]['player']['id']
            except KeyError:
                continue

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
                eventDescription = f"\'{event['result']['description']}\'"
            except KeyError:
                eventDescription = 'NULL'

            try:
                secondaryType = f"\'{event['result']['secondaryType']}\'"
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

            query = f"insert into live_feed values (" \
                    f"{eventID}," \
                    f"{gameID}," \
                    f"{gameEvent}," \
                    f"{eventCode}," \
                    f"{eventTypeID}," \
                    f"{eventDescription}," \
                    f"{secondaryType}," \
                    f"{periodNum}," \
                    f"{periodTime}," \
                    f"{playerOneID}," \
                    f"{playerTwoID}," \
                    f"{xCoordinate}," \
                    f"{yCoordinate})"

            print(query)




        break


    # for game in games:
    #     # url_string = f"https://statsapi.web.nhl.com/api/v1/game/{game[0]}/feed/live"
    #     url_string = f"https://statsapi.web.nhl.com/api/v1/game/{2018020066}/feed/live"
    #     url = requests.get(url_string)
    #     url_data = url.json()
    #
    #     try:
    #         gameID = url_data['gamePk']
    #     except KeyError:
    #         gameID = 'NULL'
    #
    #     for event in url_data['liveData']['plays']['allPlays']:
    #         try:
    #             playerTwoID = event['players'][1]['player']['id']
    #         except KeyError:
    #             playerTwoID = 'NULL'
    #         except IndexError:
    #             playerTwoID = 'NULL'
    #
    #         try:
    #             playerOneID = event['players'][0]['player']['id']
    #         except KeyError:
    #             continue
    #
    #         try:
    #             gameEvent = f"\'{event['result']['event']}\'"
    #         except KeyError:
    #             gameEvent = 'NULL'
    #
    #         try:
    #             eventCode = f"\'{event['result']['eventCode']}\'"
    #         except KeyError:
    #             eventCode = 'NULL'
    #
    #         try:
    #             eventTypeID = f"\'{event['result']['eventTypeId']}\'"
    #         except KeyError:
    #             eventTypeID = 'NULLeventTypeID'
    #
    #         try:
    #             eventDescription = f"\'{event['result']['description']}\'"
    #         except KeyError:
    #             eventDescription = 'NULL'
    #
    #         try:
    #             secondaryType = f"\'{event['result']['secondaryType']}\'"
    #         except KeyError:
    #             secondaryType = 'NULL'
    #
    #         try:
    #             periodNum = event['about']['period']
    #         except KeyError:
    #             periodNum = 'NULL'
    #
    #         eventID = event['about']['eventId']
    #
    #         try:
    #             periodTime = f"\'{event['about']['periodTime']}\'"
    #         except KeyError:
    #             periodTime = 'NULL'
    #
    #         try:
    #             xCoordinate = event['coordinates']['x']
    #         except KeyError:
    #             xCoordinate = 'NULL'
    #
    #         try:
    #             yCoordinate = event['coordinates']['y']
    #         except KeyError:
    #             yCoordinate = 'NULL'
    #
    #         query = f"insert into live_feed values (" \
    #                 f"{eventID}," \
    #                 f"{gameID}," \
    #                 f"{gameEvent}," \
    #                 f"{eventCode}," \
    #                 f"{eventTypeID}," \
    #                 f"{eventDescription}," \
    #                 f"{secondaryType}," \
    #                 f"{periodNum}," \
    #                 f"{periodTime}," \
    #                 f"{playerOneID}," \
    #                 f"{playerTwoID}," \
    #                 f"{xCoordinate}," \
    #                 f"{yCoordinate})"
    #
    #         try:
    #             cursor.execute(query)
    #             connection.commit()
    #         except IntegrityError:
    #             cursor.execute(f'select playerID from players where playerID = {playerOneID} or playerID = {playerTwoID};')
    #             oldPlayers = cursor.fetchall()
    #             oldPlayers = [i[0] for i in oldPlayers]
    #             for player in [playerOneID, playerTwoID]:
    #                 if player not in oldPlayers:
    #                     date = url_data['gameData']['datetime']['dateTime'][0:10] + " " + url_data['gameData']['datetime']['dateTime'][11:-1]
    #                     get_player(connection, player)
    #                     get_active_players(connection, player, f"\'{date}\'")
    #                     get_rookie(connection, player, f"\'{date}\'")
    #                     get_current_team(connection, player, f"\'{date}\'")
    #                     get_captain(connection, player, f"\'{date}\'")
    #                     get_position(connection, player, f"\'{date}\'")
    #                     get_alternate_captain(connection, player, f"\'{date}\'")
    #                     get_number(connection, player, f"\'{date}\'")
    #                     try:
    #                         cursor.execute(query)
    #                         connection.commit()
    #                     except:
    #                         print("")
    #
    # DatabaseConnection.mysql_close(connection)
