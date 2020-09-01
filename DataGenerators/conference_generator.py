import requests
from MySQLCode import DatabaseConnection

connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()

for conference in range(1, 8):
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/conferences/{conference}")
    url_data = url.json()
    url_data = url_data["conferences"]
    conference = url_data[0]

    conferenceID = conference['id']
    conferenceName = f"\'{conference['name']}\'"
    abbreviation = f"\'{conference['abbreviation']}\'"
    shortName = f"\'{conference['shortName']}\'"
    active = conference['active']

    query = f"insert into conferences values (" \
            f"{conferenceID}," \
            f"{conferenceName}," \
            f"{abbreviation}," \
            f"{shortName}," \
            f"{active})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

DatabaseConnection.mysql_close(connection)
