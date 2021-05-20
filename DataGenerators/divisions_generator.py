import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from datetime import date


def get_divisions():
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection('localhost', 'hockey', creds.user, creds.password)

    cursor = conn.open()
    cursor = cursor.cursor()

    div = 1
    cont = True
    while cont:
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/divisions/{div}")
        # print(f"https://statsapi.web.nhl.com/api/v1/divisions/{div}")
        url_data = url.json()
        try:
            url_data = url_data["divisions"]
        except KeyError:
            div += 1
            if div > 50:
                break
            continue
        try:
            division = url_data[0]
        except IndexError:
            div += 1
            if div > 50:
                break
            continue

        divisionID = division['id']
        divisionName = f"\'{division['name']}\'"
        abbreviation = f"\'{division['abbreviation']}\'"
        try:
            shortName = f"\'{division['nameShort']}\'"
        except KeyError:
            shortName = 'NULL'
        active = division['active']
        if active:
            active = 1
        else:
            active = 0
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
                f"\'{date.today()}\'," \
                f"{active})"
        cursor.execute(query)

        div += 1
        if div > 50:
            break

    cursor.commit()

    conn.close()
