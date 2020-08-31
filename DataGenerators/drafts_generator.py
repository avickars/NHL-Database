import requests
from MySQLCode import DatabaseConnection

years = list(range(2000, 2020))

url_string = "https://statsapi.web.nhl.com/api/v1/draft/"


# connection = DatabaseConnection.mysql_open()

for year in years:
    print("Downloading Draft Picks for year: ", year)
    url = requests.get(f"{url_string}{year}")
    print(url)
    url_data = url.json()
    url_data = url_data['drafts'][0]['rounds']


# DatabaseConnection.mysql_close(connection)
