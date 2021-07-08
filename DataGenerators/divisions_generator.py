import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd


def get_divisions():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current conferences
    divisions = pd.read_sql_query("select * from divisions", connection)

    div = 1
    cont = True
    while cont:
        # Getting division information
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/divisions/{div}")
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
        # Testing to see if we already have the division in the system
        if len(divisions[divisions['divisionID'] == divisionID]) == 0:
            divisionName = f"\'{division['name']}\'"
            abbreviation = f"\'{division['abbreviation']}\'"
            try:
                shortName = f"\'{division['nameShort']}\'"
            except KeyError:
                shortName = 'NULL'
            try:
                conferenceID = division['conference']['id']
            except KeyError:
                conferenceID = 'NULL'

            query = f"insert into divisions values (" \
                    f"{divisionID}," \
                    f"{divisionName}," \
                    f"{abbreviation}," \
                    f"{shortName}," \
                    f"{conferenceID})"
            cursor.execute(query)
            connection.commit()

        active = division['active']
        query = f"insert into division_activity (divisionID, date, active) values ({divisionID}, \'{get_time()}\', {active})"
        cursor.execute(query)
        connection.commit()

        div += 1
        if div > 50:
            break

    conn.close()
    return 0
