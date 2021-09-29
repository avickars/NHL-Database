import mysql.connector.errors as Errors


def get_new_game_lineup_templates(cursor, url_data, gameTypeID):
    numIDInstance = 0
    oldID = None
    for rosterSlot in url_data:
        query = "insert into draft_kings.contest_lineup_templates values ("
        try:
            id = rosterSlot['rosterSlot']['id']
            if id is None:
                id = 'NULL'
        except KeyError:
            return -1
        if oldID == id:
            numIDInstance += 1
        else:
            numIDInstance = 0
        oldID = id
        query += f"{id},"

        try:
            name = rosterSlot['rosterSlot']['name']
        except KeyError:
            name = 'NULL'
        if name is None:
            name = 'NULL'
            query += f"{name},"
        else:
            query += f"\'{name}\',"

        try:
            description = rosterSlot['rosterSlot']['description']
        except KeyError:
            description = 'NULL'
        if description is None:
            description = 'NULL'
            query += f"{description},"
        else:
            query += f"\'{description}\',"

        try:
            positionTip = rosterSlot['rosterSlot']['positionTip']
        except KeyError:
            positionTip = 'NULL'
        if positionTip is None:
            positionTip = 'NULL'
            query += f"{positionTip},"
        else:
            query += f"\'{positionTip}\',"

        try:
            positionTipSubtext = rosterSlot['rosterSlot']['positionTipSubtext']
            if positionTipSubtext is None:
                positionTipSubtext = 'NULL'
            else:
                positionTipSubtext = str(positionTipSubtext).replace('x', '')
        except KeyError:
            positionTipSubtext = 'NULL'
        query += f"{positionTipSubtext},"

        try:
            if rosterSlot['rosterSlot']['notScoring']:
                notScoring = 1
            elif rosterSlot['rosterSlot']['notScoring'] is None:
                notScoring = 'NULL'
            else:
                notScoring = 0
        except KeyError:
            notScoring = 'NULL'
        query += f"{notScoring},"

        query += f"{gameTypeID},{numIDInstance})"

        try:
            cursor.execute(query)
        except Errors.DataError:
            print(query)
            return -1
        except Errors.ProgrammingError:
            print(query)
            return -1
        except Errors.IntegrityError:
            print(query)
            return -1

