import requests
from MySQLCode import DatabaseConnection

years = list(range(2000, 2020))

url_string = "https://statsapi.web.nhl.com/api/v1/draft/prospects"

connection = DatabaseConnection.mysql_open()

url = requests.get(url_string)
url_data = url.json()
url_data = url_data['prospects']

for prospect in url_data:
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
        height = prospect['height'].replace('\"', '')
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

    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except:
        print("Unable to execute: ", query)
    connection.commit()

DatabaseConnection.mysql_close(connection)
