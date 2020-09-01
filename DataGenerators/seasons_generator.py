import requests
from MySQLCode import DatabaseConnection

years = list(range(2000, 2020))

url_string = "https://statsapi.web.nhl.com/api/v1/seasons"

connection = DatabaseConnection.mysql_open()

url = requests.get(url_string)
url_data = url.json()
url_data = url_data['seasons']

for season in url_data:

    seasonID = season['seasonId']

    regularSeasonStartDate = f"\'{season['regularSeasonStartDate']}\'"

    regularSeasonEndDate = f"\'{season['regularSeasonEndDate']}\'"

    seasonEndDate = f"\'{season['seasonEndDate']}\'"

    numberOfGames = season['numberOfGames']

    tiesInUse = season['tiesInUse']

    olympicsParticipation = season['olympicsParticipation']

    conferencesInUse = season['conferencesInUse']

    divisionsInUse = season['divisionsInUse']

    wildCardInUse = season['wildCardInUse']

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

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

DatabaseConnection.mysql_close(connection)