import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from datetime import date

creds = DBC.DataBaseCredentials()
conn = DatabaseConnection.sql_connection('homeserver', 'hockey', creds.user, creds.password)

cursor = conn.open()
cursor = cursor.cursor()

conf = 1
cont = True
while cont:

    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/conferences/{conf}")
    url_data = url.json()
    try:
        url_data = url_data["conferences"]
    except KeyError:
        break
    conference = url_data[0]
    conferenceID = conference['id']
    conferenceName = f"\'{conference['name']}\'"
    abbreviation = f"\'{conference['abbreviation']}\'"
    shortName = f"\'{conference['shortName']}\'"
    active = conference['active']
    if active:
        active = 1
    else:
        active = 0

    query = f"insert into conferences values (" \
            f"{conferenceID}," \
            f"{conferenceName}," \
            f"{abbreviation}," \
            f"{shortName}," \
            f"{active}," \
            f"\'{date.today()}\')"
    cursor.execute(query)

    conf += 1


cursor.commit()

conn.close()


