import requests
from MySQLCode import DatabaseConnection

connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()

for division in range(1, 19):
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/divisions/{division}")
    url_data = url.json()
    url_data = url_data["divisions"]
    division = url_data[0]

    divisionID = division['id']
    divisionName = f"\'{division['name']}\'"
    abbreviation = f"\'{division['abbreviation']}\'"
    try:
        shortName = f"\'{division['nameShort']}\'"
    except KeyError:
        shortName = 'NULL'
    active = division['active']
    try:
        conferenceID = division['conference']['id']
    except KeyError:
        conferenceID = 'NULL'

    query = f"insert into divisions values (" \
            f"{divisionID}," \
            f"{divisionName}," \
            f"{abbreviation}," \
            f"{shortName}," \
            f"{conferenceID}," \
            f"{active})"

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

DatabaseConnection.mysql_close(connection)
