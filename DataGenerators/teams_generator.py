import requests
from SQLCode import DatabaseConnection

connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()

for team in range(1, 59):
    if team == 55:
        continue
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{team}")
    url_data = url.json()
    url_data = url_data["teams"]
    team = url_data[0]

    try:
        teamID = team['id']
    except KeyError:
        teamID = 'NULL'

    try:
        venueName = f"\"{team['venue']['name']}\""
    except KeyError:
        venueName = 'NULL'

    try:
        venueCity = f"\"{team['venue']['city']}\""
    except KeyError:
        venueCity = 'NULL'

    try:
        timeZone = f"\"{team['venue']['timeZone']['id']}\""
    except KeyError:
        timeZone = 'NULL'

    try:
        abbreviation = f"\"{team['abbreviation']}\""
    except KeyError:
        abbreviation = 'NULL'

    try:
        divisionID = team['division']['id']
    except KeyError:
        divisionID = 'NULL'

    try:
        officialSiteUrl = f"\"{team['officialSiteUrl']}\""
    except KeyError:
        officialSiteUrl = 'NULL'

    try:
        franchiseID = team['franchise']['franchiseId']
    except KeyError:
        franchiseID = 'NULL'

    try:
        active = team['active']
    except KeyError:
        active = 'NULL'

    query = f"insert into teams values({teamID}, " \
            f"{venueName}, " \
            f"{venueCity}, " \
            f"{timeZone}, " \
            f"{abbreviation}," \
            f"{divisionID}," \
            f"{officialSiteUrl}," \
            f"{franchiseID}," \
            f"{active})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

DatabaseConnection.mysql_close(connection)
