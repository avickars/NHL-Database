import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import mysql.connector.errors as Errors

from datetime import date, datetime


def get_current_seasonID():
    currentYear = int(datetime.now().strftime("%Y"))
    today = date.today()

    jan1 = datetime.strptime('Jan 1', '%b %d').date().replace(year=today.year)

    if today >= jan1:
        return f"{currentYear - 1}{currentYear}"
    else:
        return f"{currentYear}{currentYear + 1}"


def get_teams(teamID):
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current teams
    teams = pd.read_sql_query("select * from teams", connection)

    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{teamID}")
    url_data = url.json()
    try:
        url_data = url_data["teams"]
    except KeyError:
        return
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
        connection.commit()
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
        connection.commit()

    # Updating whether or not the team is active
    try:
        active = team['active']
    except KeyError:
        active = 'NULL'
    query = f"insert into team_activity (teamID, date, active) values ({teamID}, \'{get_time()}\', {active})"
    cursor.execute(query)
    connection.commit()

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
    print('Here5')
    cursor.execute(query)
    connection.commit()

    # Updating the teams division
    try:
        divisionID = f"{team['division']['id']}"
    except KeyError:
        divisionID = 'NULL'
    query = f"insert into team_plays_in_division values ({teamID}, {divisionID}, '{get_time()}')"
    cursor.execute(query)
    connection.commit()
    connection.close()


def get_schedule():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current season
    seasons = pd.read_sql_query('select seasonID from seasons where regularSeasonStartDate>=\'2000-10-04\';', connection)

    for index, season in seasons.iterrows():
        print(season[0])

        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?season={season[0]}")
        url_data = url.json()
        for date in url_data['dates']:
            # To delete this later, only keeping for now
            if not datetime.strptime(date['date'], '%Y-%m-%d').date() < datetime.today().date():
                continue

            gameDate = f"\'{date['date']}\'"

            for game in date['games']:
                gameID = game['gamePk']

                gameType = f"\'{game['gameType']}\'"

                homeTeamID = game['teams']['home']['team']['id']

                awayTeamID = game['teams']['away']['team']['id']

                query = f"insert into schedules values (" \
                        f"{season[0]}," \
                        f"{gameID}," \
                        f"{gameType}," \
                        f"{gameDate}," \
                        f"{homeTeamID}," \
                        f"{awayTeamID})"

                cursor = connection.cursor()
                # Trying to execute the query
                try:
                    cursor.execute(query)
                    connection.commit()
                except Errors.IntegrityError:
                    # I found there were a lot of outlier teams that I didn't catch in teams_generator, so adding them in here
                    print(query)
                    connection.rollback()
                    get_teams(homeTeamID)
                    get_teams(awayTeamID)
                    cursor.execute(query)
                    connection.commit()
                except Errors.ProgrammingError:
                    print(query)
                    return -1

    conn.close()


get_schedule()
