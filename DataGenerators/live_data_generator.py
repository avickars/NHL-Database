from MySQLCode import DatabaseConnection
from mysql.connector.errors import IntegrityError
from DataGenerators.players_generator import get_player, get_active_players, get_rookie, get_current_team, get_captain, get_position, get_alternate_captain, get_number
import requests

connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()
cursor.execute('select gameID from schedules')
games = cursor.fetchall()

for game in games:
    # url_string = f"https://statsapi.web.nhl.com/api/v1/game/{game[0]}/feed/live"
    url_string = f"https://statsapi.web.nhl.com/api/v1/game/{2018020066}/feed/live"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        gameID = url_data['gamePk']
    except KeyError:
        gameID = 'NULL'

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

        try:
            cursor.execute(query)
            connection.commit()
        except IntegrityError:
            cursor.execute(f'select playerID from players where playerID = {playerOneID} or playerID = {playerTwoID};')
            oldPlayers = cursor.fetchall()
            oldPlayers = [i[0] for i in oldPlayers]
            for player in [playerOneID, playerTwoID]:
                if player not in oldPlayers:
                    date = url_data['gameData']['datetime']['dateTime'][0:10] + " " + url_data['gameData']['datetime']['dateTime'][11:-1]
                    get_player(connection, player)
                    get_active_players(connection, player, f"\'{date}\'")
                    get_rookie(connection, player, f"\'{date}\'")
                    get_current_team(connection, player, f"\'{date}\'")
                    get_captain(connection, player, f"\'{date}\'")
                    get_position(connection, player, f"\'{date}\'")
                    get_alternate_captain(connection, player, f"\'{date}\'")
                    get_number(connection, player, f"\'{date}\'")
                    try:
                        cursor.execute(query)
                        connection.commit()
                    except:
                        print("")

DatabaseConnection.mysql_close(connection)
