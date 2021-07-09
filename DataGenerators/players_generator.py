import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time
import mysql.connector.errors as Errors


def get_new_players():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the current players (checking the live feed for new players)
    print('Getting New Players')
    players = pd.read_sql_query("select distinct playerID from live_feed where playerID not in (select playerID from players)", connection)
    print(players)

    for index, playerID in players.iterrows():
        playerID = playerID.values[0]
        if get_player(connection, playerID) == -1:
            return -1
        get_other_player_info(connection, playerID, f"\'{get_time()}\'")
        break

    # Getting the current players (checking the box_scores for new players)
    players = pd.read_sql_query("select distinct playerID from box_scores where playerID not in (select playerID from players)", connection)

    for index, playerID in players.iterrows():
        playerID = playerID.values[0]
        get_player(connection, playerID)
        get_other_player_info(connection, playerID, f"\'{get_time()}\'")

    conn.close()


def get_headshots(connection, playerID):
    cursor = connection.cursor()

    headshotURL = f"\'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{playerID}.jpg\'"

    query = f"insert into head_shots values ({playerID}, {headshotURL}, \'{get_time()}\')"

    try:
        cursor.execute(query)
        connection.commit()
    except Errors.DataError:
        print("ERROR")
        print(query)
        return -1
    except Errors.ProgrammingError:
        print("ERROR")
        print(query)
        return -1


def update_players():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the current conferences
    players = pd.read_sql_query("select playerID from players", connection)

    for index, playerID in players.iterrows():
        playerID = playerID.values[0]
        get_other_player_info(connection, playerID, f"\'{get_time()}\'")

    conn.close()


def get_player(connection, playerID):
    print(playerID)
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    try:
        firstName = f"{player['firstName']}"
        firstName = firstName
        # firstName = firstName.replace("\'", " ")
        firstName = "\"" + firstName + "\""
    except KeyError:
        firstName = 'NULL'

    try:
        lastName = f"\'{player['lastName']}\'"
        lastName = lastName
        # lastName = lastName.replace("\'", " ")
        lastName = "\"" + lastName + "\""
    except KeyError:
        lastName = 'NULL'

    try:
        birthDate = f"\"{player['birthDate']}\""
    except KeyError:
        birthDate = 'NULL'

    try:
        birthCity = f"{player['birthCity']}"
        birthCity = birthCity
        # birthCity = birthCity.replace("\'", " ")
        birthCity = "\"" + birthCity + "\""
    except KeyError:
        birthCity = 'NULL'

    try:
        birthStateProvince = f"{player['birthStateProvince']}"
        birthStateProvince = birthStateProvince
        # birthStateProvince = birthStateProvince.replace("\'", " ")
        birthStateProvince = "\"" + birthStateProvince + "\""
    except KeyError:
        birthStateProvince = 'NULL'

    try:
        birthCountry = f"\'{player['birthCountry']}\'"
        birthCountry = birthCountry
        # birthCountry = birthCountry.replace("\'", " ")
        birthCountry = "\"" + birthCountry + "\""
    except KeyError:
        birthCountry = 'NULL'

    try:
        height = player['height']
        height = player['height'].replace('\"', '')
        height = f"\"{height}\""
    except KeyError:
        height = 'NULL'

    try:
        shootsCatches = f"\"{player['shootsCatches']}\""
    except KeyError:
        shootsCatches = 'NULL'

    query = f"insert into players values (" \
            f"{playerID}," \
            f"{firstName}," \
            f"{lastName}," \
            f"{birthDate}," \
            f"{birthCity}," \
            f"{birthStateProvince}," \
            f"{birthCountry}," \
            f"{height}," \
            f"{shootsCatches})"

    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Errors.ProgrammingError:
        print(query)
        return -1
    connection.commit()


def get_other_player_info(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    get_weight(connection, playerID, date, player)
    get_active_players(connection, playerID, date, player)
    get_rookie(connection, playerID, date, player)
    # get_current_team(connection, playerID, date, player)
    get_captain(connection, playerID, date, player)
    get_position(connection, playerID, date, player)
    get_alternate_captain(connection, playerID, date, player)
    get_number(connection, playerID, date, player)
    get_roster_status(connection, playerID, date, player)


def get_roster_status(connection, playerID, date, player):
    try:
        rosterStatus = player['rosterStatus']
    except KeyError:
        rosterStatus = 'N'
    query = f"insert into roster_status values (" \
            f"{playerID}," \
            f"\"{rosterStatus}\"," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_weight(connection, playerID, date, player):
    try:
        weight = player['weight']
    except KeyError:
        weight = 'NULL'

    query = f"insert into player_weighs values (" \
            f"{playerID}," \
            f"{weight}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_active_players(connection, playerID, date, player):
    try:
        active = player['active']
    except KeyError:
        active = False

    query = f"insert into player_active values (" \
            f"{playerID}," \
            f"{active}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_rookie(connection, playerID, date, player):
    try:
        rookie = player['rookie']
    except KeyError:
        rookie = 'NULL'

    query = f"insert into rookies values (" \
            f"{playerID}," \
            f"{rookie}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_current_team(connection, playerID, date, player):
    try:
        currentTeamID = player['currentTeam']['id']
    except KeyError:
        currentTeamID = 'NULL'

    query = f"insert into plays_for values (" \
            f"{playerID}," \
            f"{currentTeamID}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_captain(connection, playerID, date, player):
    try:
        captain = player['captain']
    except KeyError:
        captain = 'NULL'

    query = f"insert into captain values (" \
            f"{playerID}," \
            f"{captain}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_position(connection, playerID, date, player):
    try:
        primaryPositionCode = f"\"{player['primaryPosition']['code']}\""
    except KeyError:
        primaryPositionCode = 'NULL'

    try:
        primaryPositionName = f"\"{player['primaryPosition']['name']}\""
    except KeyError:
        primaryPositionName = 'NULL'

    try:
        primaryPositionType = f"\"{player['primaryPosition']['type']}\""
    except KeyError:
        primaryPositionType = 'NULL'

    cursor = connection.cursor()

    query = f"insert into plays_position values (" \
            f"{playerID}," \
            f"{primaryPositionCode}," \
            f"{date})"

    try:
        cursor.execute(query)
        connection.rollback()
    except Errors.IntegrityError:
        cursor.execute(f"insert into positions values ("
                       f"{primaryPositionCode},"
                       f"{primaryPositionName},"
                       f"{primaryPositionType})")
        connection.commit()

        cursor.execute(query)
        connection.commit()


def get_alternate_captain(connection, playerID, date, player):
    try:
        alternateCaptain = player['alternateCaptain']
    except KeyError:
        alternateCaptain = 'NULL'

    query = f"insert into alternate_captain values (" \
            f"{playerID}," \
            f"{alternateCaptain}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_number(connection, playerID, date, player):
    try:
        primaryNumber = f"\"{player['primaryNumber']}\""
    except KeyError:
        primaryNumber = 'NULL'

    query = f"insert into wears_number values (" \
            f"{playerID}," \
            f"{primaryNumber}," \
            f"{date})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
