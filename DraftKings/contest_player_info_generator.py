import pandas as pd
import requests
import mysql.connector.errors as Errors
from datetime import datetime

def get_player_info_api(cursor, connection):
    contests = pd.read_sql_query(f"select contestID, draftGroupId from draft_kings.contest_details where contestStartTime >= CONVERT_TZ(\'{datetime.today().date()} 0:00:00\','right/US/Pacific','UTC') and contestStartTime <= CONVERT_TZ(\'{datetime.today().date()} 23:59:59\','right/US/Pacific','UTC')", connection)

    for index, contest in contests.iterrows():
        print(contest['contestID'])
        url_string = f"https://api.draftkings.com/draftgroups/v1/draftgroups/{contest['draftGroupId']}/draftables"
        url = requests.get(url_string)
        url_data = url.json()

        stats = pd.read_sql_query(f"select id from draft_kings.draft_stats", connection)

        for draftStat in url_data['draftStats']:
            if draftStat['id'] not in stats['id'].values:
                cursor.execute(f"insert into draft_kings.draft_stats values ({draftStat['id']}, \'{draftStat['abbr']}\', \'{draftStat['name']}\', \'{draftStat['order']}\')")
                connection.commit()

        draftTables = url_data['draftables']

        for player in draftTables:
            query = "insert into draft_kings.draft_groups_players_api values ("
            try:
                draftableId = player['draftableId']
            except KeyError:
                draftableId = 'NULL'
            if draftableId is None:
                draftableId = 'NULL'
            query += f"{draftableId},"

            try:
                firstName = player['firstName'].replace("\'", ' ')
            except KeyError:
                firstName = 'NULL'
            if firstName is None:
                firstName = 'NULL'
                query += f"{firstName},"
            elif firstName != 'NULL':
                query += f"\"{firstName}\","

            try:
                lastName = player['lastName']
            except KeyError:
                lastName = 'NULL'
            if lastName is None:
                lastName = 'NULL'
                query += f"{lastName},"
            elif lastName != 'NULL':
                query += f"\"{lastName}\","

            try:
                displayName = player['displayName']
            except KeyError:
                displayName = 'NULL'
            if displayName is None:
                displayName = 'NULL'
                query += f"{displayName},"
            elif displayName != 'NULL':
                query += f"\"{displayName}\","

            try:
                shortName = player['shortName']
            except KeyError:
                shortName = 'NULL'
            if shortName is None:
                shortName = 'NULL'
                query += f"{shortName},"
            elif shortName != 'NULL':
                query += f"\"{shortName}\","

            try:
                playerId = player['playerId']
            except KeyError:
                playerId = 'NULL'
            if playerId is None:
                playerId = 'NULL'
            query += f"{playerId},"

            try:
                playerDkId = player['playerDkId']
            except KeyError:
                playerDkId = 'NULL'
            if playerDkId is None:
                playerDkId = 'NULL'
            query += f"{playerDkId},"

            try:
                position = player['position']
            except KeyError:
                position = 'NULL'
            if position is None:
                position = 'NULL'
                query += f"{position},"
            elif position != 'NULL':
                query += f"\'{position}\',"

            try:
                rosterSlotId = player['rosterSlotId']
            except KeyError:
                rosterSlotId = 'NULL'
            if rosterSlotId is None:
                rosterSlotId = 'NULL'
            query += f"{rosterSlotId},"

            try:
                salary = player['salary']
            except KeyError:
                salary = 'NULL'
            if salary is None:
                salary = 'NULL'
            query += f"{salary},"

            try:
                teamAbbreviation = player['teamAbbreviation']
            except KeyError:
                teamAbbreviation = 'NULL'
            if teamAbbreviation is None:
                teamAbbreviation = 'NULL'
                teamAbbreviation += f"{teamAbbreviation},"
            elif teamAbbreviation != 'NULL':
                query += f"\'{teamAbbreviation}\',"

            for draftStatAttribute in player['draftStatAttributes']:

                try:
                    sortvalue = draftStatAttribute['sortValue']
                except KeyError:
                    sortvalue = 'NULL'
                if sortvalue is None:
                    sortvalue = 'NULL'
                elif sortvalue != 'NULL':
                    sortvalue = f"\'{sortvalue}\'"

                try:
                    value = draftStatAttribute['value']
                except KeyError:
                    value = 'NULL'
                if value is None:
                    value = 'NULL'
                elif value != 'NULL':
                    value = f"\'{value}\'"

                try:
                    quality = draftStatAttribute['quality']
                except KeyError:
                    quality = 'NULL'
                if quality is None:
                    quality = 'NULL'
                elif quality != 'NULL':
                    quality = f"\'{quality}\'"

                try:
                    cursor.execute(f"insert into draft_kings.draft_stats_players values ({draftStatAttribute['id']}, {contest['contestID']}, {value}, {sortvalue}, {quality}, {playerId})")
                except:
                    print(f"insert into draft_kings.draft_stats_players values ({draftStatAttribute['id']}, {contest['contestID']}, {value}, {sortvalue}, {quality}, {playerId})")
                    return -1

            query += f"{contest['contestID']})"

            try:
                cursor.execute(query)
            except Errors.ProgrammingError:
                print(query)
                return -1
