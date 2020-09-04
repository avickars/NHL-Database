import requests


def get_player(connection, playerID):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    try:
        firstName = f"\'{player['firstName']}\'"
    except KeyError:
        firstName = 'NULL'

    try:
        lastName = f"\'{player['lastName']}\'"
    except KeyError:
        lastName = 'NULL'

    try:
        primaryNumber = player['primaryNumber']
    except KeyError:
        primaryNumber = 'NULL'

    try:
        birthDate = f"\'{player['birthDate']}\'"
    except KeyError:
        birthDate = 'NULL'

    try:
        birthCity = f"\'{player['birthCity']}\'"
    except KeyError:
        birthCity = 'NULL'

    try:
        birthStateProvince = f"\'{player['birthStateProvince']}\'"
    except KeyError:
        birthStateProvince = 'NULL'

    try:
        birthCountry = f"\'{player['birthCountry']}\'"
    except KeyError:
        birthCountry = 'NULL'

    try:
        height = player['height'].replace('\"', '')
        height = f"\"{height}\""
    except KeyError:
        height = 'NULL'

    try:
        weight = player['weight']
    except KeyError:
        weight = 'NULL'

    try:
        shootsCatches = f"\'{player['shootsCatches']}\'"
    except KeyError:
        shootsCatches = 'NULL'

    try:
        rosterStatus = f"\'{player['rosterStatus']}\'"
    except KeyError:
        rosterStatus = 'NULL'

    query = f"insert into players values (" \
            f"{playerID}," \
            f"{firstName}," \
            f"{lastName}," \
            f"{birthDate}," \
            f"{birthCity}," \
            f"{birthStateProvince}," \
            f"{birthCountry}," \
            f"{height}," \
            f"{weight}," \
            f"{shootsCatches}," \
            f"{rosterStatus})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_active_players(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    try:
        active = player['active']
    except KeyError:
        active = 'NULL'

    query = f"insert into active values (" \
            f"{playerID}," \
            f"{active}," \
            f"{date})"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_rookie(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

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


def get_current_team(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

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


def get_captain(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

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


def get_position(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    try:
        primaryPositionCode = f"\'{player['primaryPosition']['code']}\'"
    except KeyError:
        primaryPositionCode = 'NULL'

    try:
        primaryPositionName = f"\'{player['primaryPosition']['name']}\'"
    except KeyError:
        primaryPositionName = 'NULL'

    try:
        primaryPositionType = f"\'{player['primaryPosition']['type']}\'"
    except KeyError:
        primaryPositionType = 'NULL'

    query = f"insert into position values (" \
            f"{playerID}," \
            f"{primaryPositionCode}," \
            f"{primaryPositionName}," \
            f"{primaryPositionType}," \
            f"{date})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def get_alternate_captain(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return
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


def get_number(connection, playerID, date):
    url_string = f"https://statsapi.web.nhl.com/api/v1/people/{playerID}"
    url = requests.get(url_string)
    url_data = url.json()

    try:
        player = url_data['people'][0]
    except KeyError:
        return

    try:
        primaryNumber = f"\'{player['primaryNumber']}\'"
    except KeyError:
        primaryNumber = 'NULL'

    query = f"insert into wears_number values (" \
            f"{playerID}," \
            f"{primaryNumber}," \
            f"{date})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
