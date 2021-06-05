import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time
import datetime
import numpy as np
import pyodbc
from dateutil.relativedelta import relativedelta


def get_drafts():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select top 1 date from script_execution where script = 'get_drafts' order by date desc",
                                      connection)

    # If we've never run it before, we start from the beginning
    if len(mostRecentRun) == 0:
        date_time_str = '2000-10-04 01:55:19'
        mostRecentRun = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        mostRecentRun = mostRecentRun.date()
    else:
        # Otherwise just converting it into sql form
        # Converting it from np.datetime64 to datetime
        # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
        mostRecentRun = mostRecentRun.date()

    while mostRecentRun.year <= datetime.datetime.today().date().year:
        print("Downloading Draft Picks for year: ", mostRecentRun.year)
        url = requests.get(f"https://statsapi.web.nhl.com/api/v1/draft/{mostRecentRun.year}")
        url_data = url.json()
        try:
            # Expecting this error when we hit the current draft year, so we bail out
            url_data = url_data['drafts'][0]['rounds']
        except KeyError:
            break
        for draftRound in url_data:
            for pick in draftRound['picks']:
                try:
                    draftYear = pick['year']
                except KeyError:
                    draftYear = 'NULL'

                try:
                    pickRound = pick['round']
                except KeyError:
                    pickRound = 'NULL'

                try:
                    pickOverall = pick['pickOverall']
                except KeyError:
                    pickOverall = 'NULL'

                try:
                    pickInRound = pick['pickInRound']
                except KeyError:
                    pickInRound = 'NULL'

                try:
                    teamID = pick['team']['id']
                except KeyError:
                    teamID = 'NULL'

                try:
                    prospectID = pick['prospect']['id']
                except KeyError:
                    prospectID = 'NULL'

                try:
                    fullName = pick['prospect']['fullName'].replace('\'', '\"')
                    fullName = f"\'{fullName}\'"
                except KeyError:
                    fullName = 'NULL'

                query = f'insert into draft_picks values (' \
                        f'{draftYear},' \
                        f'{pickRound},' \
                        f'{pickOverall},' \
                        f'{pickInRound},' \
                        f'{teamID},' \
                        f'{prospectID},' \
                        f'{fullName})'
                try:
                    cursor.execute(query)
                    connection.commit()
                except pyodbc.ProgrammingError:
                    print("Error")
                    print(query)
                    return -1

        # Incrementing the most recent run, since we have now updated the draft to include the year for mostRecentRun
        mostRecentRun = mostRecentRun + relativedelta(years=1)

    conn.close()


def update_prospects():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the current conferences
    players = pd.read_sql_query("select * from (select distinct prospectID from draft_picks where prospectID not in (select prospectID from prospects) ) P where ISNULL(P.prospectID,1) <> 1", connection)

    for index, prospectID in players.iterrows():
        prospectID = prospectID.values[0]
        update_prospect_table(prospectID, connection)

    conn.close()


def update_prospect_table(pID, connection):
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/draft/prospects/{pID}")
    url_data = url.json()
    url_data = url_data['prospects']
    prospect = url_data[0]

    try:
        prospectID = prospect['id']
    except KeyError:
        prospectID = 'NULL'

    try:
        firstName = prospect['firstName'].replace('\'', '\"')
        firstName = f"\'{firstName}\'"
    except KeyError:
        firstName = 'NULL'

    try:
        lastName = prospect['lastName'].replace('\'', '\"')
        lastName = f"\'{lastName}\'"
    except KeyError:
        lastName = 'NULL'

    try:
        birthDate = f"\'{prospect['birthDate']}\'"
    except KeyError:
        birthDate = 'NULL'

    try:
        birthCity = prospect['birthCity'].replace('\'', '\"')
        birthCity = f"\'{birthCity}\'"
        if birthCity == "\'\'":
            birthCity = 'NULL'
    except KeyError:
        birthCity = 'NULL'

    try:
        birthStateProvince = prospect['birthStateProvince'].replace('\'', '\"')
        birthStateProvince = f"\'{birthStateProvince}\'"
    except KeyError:
        birthStateProvince = 'NULL'

    try:
        birthCountry = prospect['birthCountry'].replace('\'', '\"')
        birthCountry = f"\'{birthCountry}\'"
    except KeyError:
        birthCountry = 'NULL'

    try:
        height = prospect['height'].replace('\'', '"')
        height = f"\'{height}\'"
    except KeyError:
        height = 'NULL'

    try:
        weight = prospect['weight']
    except KeyError:
        weight = 'NULL'

    try:
        shoots = f"\'{prospect['shootsCatches']}\'"
    except KeyError:
        shoots = 'NULL'

    try:
        position = f"\'{prospect['primaryPosition']['code']}\'"
        if position == "\'N/A\'":
            position = 'NULL'
    except KeyError:
        position = 'NULL'

    try:
        nhlPlayerID = prospect['nhlPlayerId']
    except KeyError:
        nhlPlayerID = 'NULL'

    try:
        prospectCategoryID = prospect['prospectCategory']['id']
    except KeyError:
        prospectCategoryID = 'NULL'

    try:
        prospectCategoryName = f"\'{prospect['prospectCategory']['name']}\'"
    except KeyError:
        prospectCategoryName = 'NULL'

    try:
        amateurTeam = prospect['amateurTeam']['name'].replace('\'', '\"')
        amateurTeam = f"\'{amateurTeam}\'"
    except KeyError:
        amateurTeam = 'NULL'

    try:
        amateurLeague = prospect['amateurLeague']['name'].replace('\'', '\"')
        amateurLeague = f"\'{amateurLeague}\'"
    except KeyError:
        amateurLeague = 'NULL'

    query = f"insert into prospects values (" \
            f"{prospectID}, " \
            f"{firstName}, " \
            f"{lastName}, " \
            f"{birthDate}, " \
            f"{birthCity}, " \
            f"{birthStateProvince}, " \
            f"{birthCountry}, " \
            f"{height}, " \
            f"{weight}," \
            f"{shoots}," \
            f"{position}," \
            f"{nhlPlayerID}," \
            f"{prospectCategoryID}," \
            f"{prospectCategoryName}," \
            f"{amateurTeam}," \
            f"{amateurLeague})"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except pyodbc.ProgrammingError:
        print("ERROR")
        print(query)
        return -1
