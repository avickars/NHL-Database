import requests
from SQLCode import DatabaseConnection
from datetime import datetime

connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()
cursor.execute('select seasonID from seasons where regularSeasonStartDate>=\'2000-10-04\';')
seasons = cursor.fetchall()

for season in seasons:
    print(season[0])
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/schedule?season={season[0]}")
    url_data = url.json()
    for date in url_data['dates']:
        if not datetime.strptime(date['date'], '%Y-%m-%d').date() < datetime.today().date():
            continue
        gameDate = f"\'{date['date']}\'"
        for game in date['games']:
            gameID = game['gamePk']

            gameType = f"\'{game['gameType']}\'"

            homeTeamID = game['teams']['home']['team']['id']

            awayTeamID = game['teams']['away']['team']['id']

            query = f"insert into schedules values (" \
                    f"{gameID}," \
                    f"{gameType}," \
                    f"{gameDate}," \
                    f"{homeTeamID}," \
                    f"{awayTeamID})"

            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

DatabaseConnection.mysql_close(connection)
