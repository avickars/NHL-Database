import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
import numpy as np


def get_seasons():

    url_string = "https://statsapi.web.nhl.com/api/v1/seasons"

    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    url = requests.get(url_string)
    url_data = url.json()
    url_data = url_data['seasons']

    # Getting the current conferences
    seasons = pd.read_sql_query("select * from seasons", connection)

    for season in url_data:

        seasonID = np.int64(season['seasonId'])

        regularSeasonStartDate = f"\'{season['regularSeasonStartDate']}\'"

        regularSeasonEndDate = f"\'{season['regularSeasonEndDate']}\'"

        seasonEndDate = f"\'{season['seasonEndDate']}\'"

        numberOfGames = season['numberOfGames']

        tiesInUse = season['tiesInUse']
        if tiesInUse:
            tiesInUse = 1
        else:
            tiesInUse = 0

        olympicsParticipation = season['olympicsParticipation']
        if olympicsParticipation:
            olympicsParticipation = 1
        else:
            olympicsParticipation = 0

        conferencesInUse = season['conferencesInUse']
        if conferencesInUse:
            conferencesInUse = 1
        else:
            conferencesInUse = 0

        divisionsInUse = season['divisionsInUse']
        if divisionsInUse:
            divisionsInUse = 1
        else:
            divisionsInUse = 0

        wildCardInUse = season['wildCardInUse']
        if wildCardInUse:
            wildCardInUse = 1
        else:
            wildCardInUse = 0

        if len(seasons[seasons['seasonID'] == seasonID]) == 0:
            query = f"insert into seasons values (" \
                    f"{seasonID}," \
                    f"{regularSeasonStartDate}," \
                    f"{regularSeasonEndDate}," \
                    f"{seasonEndDate}," \
                    f"{numberOfGames}," \
                    f"{tiesInUse}," \
                    f"{olympicsParticipation}," \
                    f"{conferencesInUse}," \
                    f"{divisionsInUse}," \
                    f"{wildCardInUse})"
        else:
            query = f"update seasons" \
                  f" set seasonID = {seasonID}," \
                  f"regularSeasonStartDate = {regularSeasonStartDate}," \
                  f"regularSeasonEndDate = {regularSeasonEndDate}," \
                  f"seasonEndDate = {seasonEndDate}," \
                  f"numberOfGames = {numberOfGames}," \
                  f"tiesInUse = {tiesInUse}," \
                  f"olympic_participation = {olympicsParticipation}," \
                  f"conferences_in_use = {conferencesInUse}," \
                  f"wild_card_in_use = {wildCardInUse}" \
                    f" where seasonID = {seasonID}"

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    conn.close()
    return 0