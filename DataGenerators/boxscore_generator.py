import requests
from MySQLCode import DatabaseConnection


connection = DatabaseConnection.mysql_open()

cursor = connection.cursor()
cursor.execute('select gameID from schedules')
games = cursor.fetchall()

for game in games:
    print(f"https://statsapi.web.nhl.com/api/v1/game/{game[0]}/boxscore")
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/game/{game[0]}/boxscore")
    url_data = url.json()
    print(url_data)
    break



connection = DatabaseConnection.mysql_close(connection)