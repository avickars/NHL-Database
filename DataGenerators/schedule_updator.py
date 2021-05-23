import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time
import pandas as pd
import numpy as np
import pyodbc

# from datetime import date, datetime
import datetime


def get_current_seasonID():
    currentYear = int(datetime.datetime.now().strftime("%Y"))
    today = datetime.date.today()

    jan1 = datetime.datetime.strptime('Jan 1', '%b %d').date().replace(year=today.year)

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


def get_daily_schedule():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select top 1 date from script_execution where script = 'get_daily_schedule' order by date desc",
                                      connection)

    # Getting the games from the current season
    games = pd.read_sql_query(f"select gameID from schedules where seasonID={get_current_seasonID()}", connection)

    # Converting it from np.datetime64 to datetime
    # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
    mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
    mostRecentRun = mostRecentRun.date()
    while mostRecentRun < datetime.date.today():
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?date={mostRecentRun}")
        url_data = url.json()

        for date in url_data['dates']:
            gameDate = f"\'{date['date']}\'"

            for game in date['games']:
                gameID = game['gamePk']

                gameType = f"\'{game['gameType']}\'"

                homeTeamID = game['teams']['home']['team']['id']

                awayTeamID = game['teams']['away']['team']['id']

                season = game['season']

                # If we haven't inserted this game before, lets insert it
                if len(games[games['gameID'] == gameID]) == 0:
                    query = f"insert into schedules values (" \
                            f"{season}," \
                            f"{gameID}," \
                            f"{gameType}," \
                            f"{gameDate}," \
                            f"{homeTeamID}," \
                            f"{awayTeamID})"
                    try:
                        cursor.execute(query)
                    except pyodbc.IntegrityError:
                        get_teams(homeTeamID)
                        get_teams(awayTeamID)
                        cursor.execute(query)
                    cursor.commit()

                # Otherwise, it maybe got rescheduled, so lets update the schedule
                else:
                    query = f"update schedules" \
                            f" set seasonID = {season}," \
                            f"gameID = {gameID}," \
                            f"gameType = {gameType}," \
                            f"gameDate = {gameDate}," \
                            f"homeTeamID = {homeTeamID}," \
                            f"awayTeamID = {awayTeamID}" \
                            f" where gameID = {gameID}"
                    try:
                        cursor.execute(query)
                    except pyodbc.IntegrityError:
                        get_teams(homeTeamID)
                        get_teams(awayTeamID)
                        cursor.execute(query)
                    cursor.commit()


        # Incrementing the most recent run, since we have now updated the schedule to games up to mostRecentRun not (not including it though)
        mostRecentRun = mostRecentRun + datetime.timedelta(days=1)

    conn.close()
