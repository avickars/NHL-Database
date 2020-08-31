import requests
from MySQLCode import DatabaseConnection

years = list(range(2000, 2020))

url_string = "https://statsapi.web.nhl.com/api/v1/draft/prospects"

connection = DatabaseConnection.mysql_open()


url = requests.get(url_string)
url_data = url.json()
url_data = url_data['prospects']

i = 0

for prospect in url_data:
    try:
        prospectID = prospect['id']
    except KeyError:
        prospectID = 'NULL'

    try:
        firstName = f"\'{prospect['firstName']}\'"
    except KeyError:
        firstName = 'NULL'

    try:
        lastName = f"\'{prospect['lastName']}\'"
    except KeyError:
        lastName = 'NULL'

    try:
        birthDate = f"\'{prospect['birthDate']}\'"
    except KeyError:
        birthDate = 'NULL'

    try:
        birthCity = f"\'{prospect['birthCity']}\'"
    except KeyError:
        birthCity = 'NULL'

    try:
        birthStateProvince = f"\'{prospect['birthStateProvince']}\'"
    except KeyError:
        birthStateProvince = 'NULL'

    try:
        birthCountry = f"\'{prospect['birthCountry']}\'"
    except KeyError:
        birthCountry = 'NULL'

    try:
        nationality = f"\'{prospect['nationality']}\'"
    except KeyError:
        nationality = 'NULL'

    try:
        height = prospect['height'].replace('\"','')
        height = f"\"{height}\""
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
        amateurTeam = f"\'{prospect['amateurTeam']['name']}\'"
    except KeyError:
        amateurTeam = 'NULL'

    try:
        amateurLeague = f"\'{prospect['amateurLeague']['name']}\'"
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
            f"{nationality}, " \
            f"{height}, " \
            f"{weight}," \
            f"{shoots}," \
            f"{position}," \
            f"{nhlPlayerID}," \
            f"{prospectCategoryID}," \
            f"{prospectCategoryName}," \
            f"{amateurTeam}," \
            f"{amateurLeague})"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()



    if i > 10:
        break
    i = i + 1







DatabaseConnection.mysql_close(connection)
