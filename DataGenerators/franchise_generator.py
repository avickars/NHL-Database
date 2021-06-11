import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd


def get_franchises():
    url = requests.get("https://statsapi.web.nhl.com/api/v1/franchises")
    url_data = url.json()
    url_data = url_data["franchises"]

    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the franchises in db
    franchises = pd.read_sql_query("select * from franchises", connection)

    for franchise in url_data:
        # getting the franchise ID
        try:
            franchiseID = franchise['franchiseId']
        except KeyError:
            franchiseID = 'NULL'

        # getting the first seasonID
        try:
            firstSeasonID = franchise['firstSeasonId']
        except KeyError:
            firstSeasonID = 'NULL'

        # Getting the last seasonID
        try:
            lastSeasonID = franchise['lastSeasonId']
        except KeyError:
            lastSeasonID = 'NULL'

        # Testing if we have this franchise in the DB, if no we add it in
        if franchiseID not in franchises['franchiseID'].values:
            query = f"insert into franchises values (" \
                    f"{franchiseID}," \
                    f"{firstSeasonID}," \
                    f"{lastSeasonID})"
            cursor.execute(query)
            cursor.commit()
        # Testing if our info on the franchise is still accurate, if not we update it
        elif franchises[franchises['franchiseID'] == franchiseID]['firstSeasonID'].values[0] != firstSeasonID:
            query = f"update franchises set firstSeasonID = {firstSeasonID} where franchiseID={franchiseID}"
            cursor.execute(query)
            cursor.commit()
        # Testing if our info on the franchise is still accurate, if not we update it
        elif franchises[franchises['franchiseID'] == franchiseID]['lastSeasonID'].values[0] != lastSeasonID:
            query = f"update franchises set lastSeasonID = {lastSeasonID} where franchiseID={franchiseID}"
            cursor.execute(query)
            cursor.commit()

    conn.close()
    return 0
