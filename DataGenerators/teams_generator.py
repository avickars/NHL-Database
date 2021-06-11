import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd


def get_teams():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current teams
    teams = pd.read_sql_query("select * from teams", connection)

    for team in range(1, 125):
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{team}")
        url_data = url.json()
        try:
            url_data = url_data["teams"]
        except KeyError:
            continue
        team = url_data[0]

        try:
            teamID = team['id']
        except KeyError:
            teamID = 'NULL'

        try:
            locationName = f"\'{team['locationName']}\'"
        except KeyError:
            locationName = 'NULL'

        try:
            teamName = f"\'{team['teamName']}\'"
        except KeyError:
            teamName = 'NULL'

        try:
            abbreviation = f"\'{team['abbreviation']}\'"
        except KeyError:
            abbreviation = 'NULL'

        try:
            franchiseID = team['franchise']['franchiseId']
        except KeyError:
            franchiseID = 'NULL'

        try:
            officialSiteUrl = f"\'{team['officialSiteUrl']}\'"
        except KeyError:
            officialSiteUrl = 'NULL'

        # Testing to see if we already have the conference in the system
        if len(teams[teams['teamID'] == teamID]) == 0:
            # If no, then we add it
            query = f"insert into teams values({teamID}, " \
                    f"{locationName}, " \
                    f"{teamName}, " \
                    f"{abbreviation}, " \
                    f"{officialSiteUrl}," \
                    f"{franchiseID})"
            cursor.execute(query)
            cursor.commit()
        else:
            # Lets refresh the data in the table
            query = f"update teams " \
                    f"set locationName = {locationName}, " \
                    f"teamName = {teamName}, " \
                    f"abbreviation = {abbreviation}, " \
                    f"officialSiteUrl = {officialSiteUrl}, " \
                    f"franchiseID = {franchiseID} " \
                    f"where teamID = {teamID};"
            cursor.execute(query)
            cursor.commit()

        # Updating whether or not the team is active
        try:
            active = team['active']
        except KeyError:
            active = 'NULL'
        if active:
            active = 1
        else:
            active = 0
        query = f"insert into team_activity (teamID, date, active) values ({teamID}, \'{get_time()}\', {active})"
        cursor.execute(query)
        cursor.commit()

        # Updating the venue the team plays in
        try:
            venueName = f"\'{team['venue']['name']}\'"
        except KeyError:
            venueName = 'NULL'

        try:
            venueCity = f"\'{team['venue']['city']}\'"
        except KeyError:
            venueCity = 'NULL'

        try:
            timeZone = f"\'{team['venue']['timeZone']['id']}\'"
        except KeyError:
            timeZone = 'NULL'
        query = f"insert into team_plays_in_venue values ({venueName},{venueCity},{timeZone},'{get_time()}',{teamID})"
        cursor.execute(query)
        cursor.commit()

        # Updating the teams division
        try:
            divisionID = f"{team['division']['id']}"
        except KeyError:
            divisionID = 'NULL'
        query = f"insert into team_plays_in_division values ({teamID}, {divisionID}, '{get_time()}')"
        cursor.execute(query)
        cursor.commit()

    conn.close()
    return 0
