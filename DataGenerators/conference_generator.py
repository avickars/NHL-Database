import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time



def get_conferences():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current conferences
    conferences = pd.read_sql_query("select * from conferences", connection)

    # Iterating through all conferences (and then some just to be safe)
    conf = 1
    cont = True
    while cont:

        # Getting conference information
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/conferences/{conf}")
        url_data = url.json()
        try:
            url_data = url_data["conferences"]
        except KeyError:
            conf += 1
            if conf > 50:
                break
            continue
        conference = url_data[0]

        conferenceID = conference['id']

        # Testing to see if we already have the conference in the system
        if len(conferences[conferences['conferenceID'] == conferenceID]) == 0:
            # If no, then we add it
            conferenceName = f"\'{conference['name']}\'"
            abbreviation = f"\'{conference['abbreviation']}\'"
            shortName = f"\'{conference['shortName']}\'"

            query = f"insert into conferences values (" \
                    f"{conferenceID}," \
                    f"{conferenceName}," \
                    f"{abbreviation}," \
                    f"{shortName})"
            cursor.execute(query)
            cursor.commit()

        # Updating the conference info
        active = conference['active']
        if active:
            active = 1
        else:
            active = 0
        query = f"insert into conference_activity (conferenceID, date, active) values ({conferenceID}, \'{get_time()}\', {active})"
        cursor.execute(query)
        cursor.commit()

        conf += 1
        if conf > 50:
            break

    conn.close()
    return 0
