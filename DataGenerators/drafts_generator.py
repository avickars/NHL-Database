import requests
import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from datetime import date

years = list(range(2010, 2020))

url_string = "https://statsapi.web.nhl.com/api/v1/draft/"


def updateProspectTable(pID, connection):
    url = requests.get(f"https://statsapi.web.nhl.com/api/v1/draft/prospects/{pID}")
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
        except mysql.connector.errors.IntegrityError:
            print("Unable to execute: ", query)
        connection.commit()


connection = DatabaseConnection.mysql_open()

for year in years:
    print("Downloading Draft Picks for year: ", year)
    url = requests.get(f"{url_string}{year}")
    url_data = url.json()
    url_data = url_data['drafts'][0]['rounds']
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
                fullName = f"\"{fullName}\""
            except KeyError:
                fullName = 'NULL'

            query = f'insert into draftsPicks values (' \
                    f'{draftYear},' \
                    f'{pickRound},' \
                    f'{pickOverall},' \
                    f'{pickInRound},' \
                    f'{teamID},' \
                    f'{prospectID},' \
                    f'{fullName})'
            print(query)
            cursor = connection.cursor()
            try:
                cursor.execute(query)
            except mysql.connector.errors.IntegrityError:
                if prospectID != 'NULL':
                    updateProspectTable(prospectID, connection)
                    cursor.execute(query)

            connection.commit()

DatabaseConnection.mysql_close(connection)
