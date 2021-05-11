import requests
from SQLCode import DatabaseConnection

connection = DatabaseConnection.mysql_open()


url = requests.get("https://statsapi.web.nhl.com/api/v1/franchises")
url_data = url.json()
url_data = url_data["franchises"]

for franchise in url_data:
    try:
        franchiseID = franchise['franchiseId']
    except KeyError:
        franchiseID = 'NULL'

    try:
        firstSeasonID = franchise['firstSeasonId']
    except KeyError:
        firstSeasonID = 'NULL'

    try:
        lastSeasonID = franchise['lastSeasonId']
    except KeyError:
        lastSeasonID = 'NULL'

    try:
        mostRecentTeamID = franchise['mostRecentTeamId']
    except KeyError:
        mostRecentTeamID = 'NULL'

    try:
        teamName = f"\"{franchise['teamName']}\""
    except KeyError:
        teamName = 'NULL'

    try:
        locationName = f"\"{franchise['locationName']}\""
    except KeyError:
        locationName = 'NULL'

    query = f"insert into franchises values (" \
            f"{franchiseID}," \
            f"{firstSeasonID}," \
            f"{lastSeasonID}," \
            f"{mostRecentTeamID}," \
            f"{teamName}," \
            f"{locationName})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

DatabaseConnection.mysql_close(connection)
