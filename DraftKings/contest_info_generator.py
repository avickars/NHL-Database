import requests
import flatdict
from datetime import date
import mysql.connector.errors as Errors


def get_contests_info(cursor):
    url_string = f"https://www.draftkings.com/lobby/getcontests?sport=NHL"
    url = requests.get(url_string)
    url_data = url.json()
    contests = url_data['Contests']
    contestIDs = []
    for contest in contests:
        query = "insert into draft_kings.contests values ("
        info = flatdict.FlatDict(contest, delimiter='.')

        try:
            if info['attr.IsStarred'] == 'true':
                IsStarred = 1
            elif info['attr.IsStarred'] is None:
                IsStarred = 'NULL'
            else:
                IsStarred = 0
        except KeyError:
            IsStarred = 'NULL'
        query += f"{IsStarred},"

        id = info['id']
        contestIDs.append(id)
        query += f"{id},"

        try:
            gameType = info['gameType']
            if gameType is None:
                gameType = 'NULL'
            query += f"\'{gameType}\',"
        except KeyError:
            gameType = 'NULL'
            query += f"{gameType},"

        try:
            if info['freeWithCrowns'] == 'true':
                freeWithCrowns = 1
            elif info['freeWithCrowns'] is None:
                freeWithCrowns = 'NULL'
            else:
                freeWithCrowns = 0
        except KeyError:
            freeWithCrowns = 'NULL'
        query += f"{freeWithCrowns},"

        try:
            if info['isBonusFinalized'] == 'true':
                isBonusFinalized = 1
            elif info['isBonusFinalized'] is None:
                isBonusFinalized = 'NULL'
            else:
                isBonusFinalized = 0
        except KeyError:
            isBonusFinalized = 'NULL'
        query += f"{isBonusFinalized},"

        try:
            if info['isSnakeDraft'] == 'true':
                isSnakeDraft = 1
            elif info['isSnakeDraft'] is None:
                isSnakeDraft = 'NULL'
            else:
                isSnakeDraft = 0
        except KeyError:
            isSnakeDraft = 'NULL'
        query += f"{isSnakeDraft},"

        try:
            crownAmount = info['crownAmount']
            if crownAmount is None:
                crownAmount = 'NULL'
        except KeyError:
            crownAmount = 'NULL'
        query += f"{crownAmount},"

        try:
            if info['attr.IsWinnerTakeAll'] == 'true':
                IsWinnerTakeAll = 1
            elif info['IsWinnerTakeAll'] is None:
                IsWinnerTakeAll = 'NULL'
            else:
                IsWinnerTakeAll = 0
        except KeyError:
            IsWinnerTakeAll = 'NULL'
        query += f"{IsWinnerTakeAll},"

        query = query + f"\'{date.today()}\')"

        try:
            cursor.execute(query)
        except Errors.DataError:
            print(query)
            return -1
        except Errors.ProgrammingError:
            print(query)
            return -1

    return contestIDs
