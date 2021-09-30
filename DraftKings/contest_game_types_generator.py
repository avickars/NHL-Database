import requests
import pandas as pd
import mysql.connector.errors as Errors
from DraftKings.contest_lineup_template_generator import get_new_game_lineup_templates


def get_new_game_types(cursor, connection):
    gameTypeIDs = pd.read_sql_query(f"select distinct gameTypeId from draft_kings.contest_details where gameTypeID not in (select gameTypeID from draft_kings.contest_rules)", connection)

    for index, gameTypeID in gameTypeIDs.iterrows():
        url_string = f"https://api.draftkings.com/lineups/v1/gametypes/{int(gameTypeID)}/rules?format=json"
        url = requests.get(url_string)
        url_data = url.json()

        query = "insert into draft_kings.contest_rules values("

        if get_new_game_lineup_templates(cursor, url_data['lineupTemplate'], int(gameTypeID)) == -1:
            return -1

        try:
            gameTypeDescription = url_data['gameTypeDescription']
        except KeyError:
            gameTypeDescription = 'NULL'
        if gameTypeDescription is None:
            gameTypeDescription = 'NULL'
            query += f"{gameTypeDescription},"
        else:
            query += f"\'{gameTypeDescription}\',"

        try:
            if url_data['salaryCap']['isEnabled']:
                salaryCapIsEnabled = 1
            elif url_data['salaryCap']['isEnabled'] is None:
                salaryCapIsEnabled = 'NULL'
            else:
                salaryCapIsEnabled = 0
        except KeyError:
            salaryCapIsEnabled = 'NULL'
        query += f"{salaryCapIsEnabled},"

        try:
            salaryCapMinValue = url_data['salaryCap']['minValue']
            if salaryCapMinValue is None:
                salaryCapMinValue = 'NULL'
        except KeyError:
            salaryCapMinValue = 'NULL'
        query += f"{salaryCapMinValue},"

        try:
            salaryCapMaxValue = url_data['salaryCap']['maxValue']
            if salaryCapMaxValue is None:
                salaryCapMaxValue = 'NULL'
        except KeyError:
            salaryCapMaxValue = 'NULL'
        query += f"{salaryCapMaxValue},"

        try:
            if url_data['gameCount']['isEnabled']:
                gameCountIsEnabled = 1
            elif url_data['gameCount']['isEnabled'] is None:
                gameCountIsEnabled = 'NULL'
            else:
                gameCountIsEnabled = 0
        except KeyError:
            gameCountIsEnabled = 'NULL'
        query += f"{gameCountIsEnabled},"

        try:
            gameCountMinValue = url_data['gameCount']['minValue']
            if gameCountMinValue is None:
                gameCountMinValue = 'NULL'
        except KeyError:
            gameCountMinValue = 'NULL'
        query += f"{gameCountMinValue},"

        try:
            gameCountMaxValue = url_data['gameCount']['maxValue']
            if gameCountMaxValue is None:
                gameCountMaxValue = 'NULL'
        except KeyError:
            gameCountMaxValue = 'NULL'
        query += f"{gameCountMaxValue},"

        try:
            if url_data['teamCount']['isEnabled']:
                teamCountIsEnabled = 1
            elif url_data['teamCount']['isEnabled'] is None:
                teamCountIsEnabled = 'NULL'
            else:
                teamCountIsEnabled = 0
        except KeyError:
            teamCountIsEnabled = 'NULL'
        query += f"{teamCountIsEnabled},"

        try:
            teamCountMinValue = url_data['teamCount']['minValue']
            if teamCountMinValue is None:
                teamCountMinValue = 'NULL'
        except KeyError:
            teamCountMinValue = 'NULL'
        query += f"{teamCountMinValue},"

        try:
            teamCountMaxValue = url_data['teamCount']['maxValue']
            if teamCountMaxValue is None:
                teamCountMaxValue = 'NULL'
        except KeyError:
            teamCountMaxValue = 'NULL'
        query += f"{teamCountMaxValue},"

        try:
            if url_data['uniquePlayers']:
                uniquePlayers = 1
            elif url_data['teamCount'] is None:
                uniquePlayers = 'NULL'
            else:
                uniquePlayers = 0
        except KeyError:
            uniquePlayers = 'NULL'
        query += f"{uniquePlayers},"

        try:
            if url_data['allowLateSwap']:
                allowLateSwap = 1
            elif url_data['allowLateSwap'] is None:
                allowLateSwap = 'NULL'
            else:
                allowLateSwap = 0
        except KeyError:
            allowLateSwap = 'NULL'
        query += f"{allowLateSwap},"

        query += f"{int(gameTypeID)})"

        try:
            cursor.execute(query)
        except Errors.DataError:
            print(query)
            return -1
        except Errors.ProgrammingError:
            print(query)
            return -1
