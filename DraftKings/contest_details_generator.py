import requests
import mysql.connector.errors as Errors


def get_contest_details(cursor, contests):
    for contestID in contests:
        url_string = f"https://api.draftkings.com/contests/v1/contests/{contestID}?format=json"
        # https: // api.draftkings.com / contests / v1 / contests / 114553969  # ?format=json
        url = requests.get(url_string)
        url_data = url.json()
        contestDetails = url_data['contestDetail']

        query = "insert into draft_kings.contest_details values ("

        try:
            contestSummary = contestDetails['contestSummary']
        except KeyError:
            contestSummary = 'NULL'
        if contestSummary is None:
            contestSummary = 'NULL'
            query += f"{contestSummary}"
        else:
            query += f"\'{contestSummary}\',"

        try:
            if contestDetails['IsCashPrizeOnly'] == "true":
                isCashPrizeOnly = 1
            elif contestDetails['IsCashPrizeOnly'] is None:
                isCashPrizeOnly = 'NULL'
            else:
                isCashPrizeOnly = 0
        except KeyError:
            isCashPrizeOnly = 'NULL'
        query += f"{isCashPrizeOnly},"

        try:
            if contestDetails['scoringStyleId'] is not None:
                scoringStyleId = contestDetails['scoringStyleId']
            else:
                scoringStyleId = 'NULL'
        except KeyError:
            scoringStyleId = 'NULL'
        query += f"{scoringStyleId},"

        try:
            sport = contestDetails['sport']
            if sport is None:
                sport = 'NULL'
            query += f"\'{sport}\',"
        except KeyError:
            sport = 'NULL'
            query += f"{sport},"

        try:
            if contestDetails['isGuaranteed'] == "true":
                isGuaranteed = 1
            elif contestDetails['isGuaranteed'] is None:
                isGuaranteed = 'NULL'
            else:
                isGuaranteed = 0
        except KeyError:
            isGuaranteed = 'NULL'
        query += f"{isGuaranteed},"

        try:
            if contestDetails['isPrivate'] == "true":
                isPrivate = 1
            elif contestDetails['isPrivate'] is None:
                isPrivate = 'NULL'
            else:
                isPrivate = 0
        except KeyError:
            isPrivate = 'NULL'
        query += f"{isPrivate},"

        try:
            if contestDetails['isResizable'] == "true":
                isResizable = 1
            elif contestDetails['isResizable'] is None:
                isResizable = 'NULL'
            else:
                isResizable = 0
        except KeyError:
            isResizable = 'NULL'
        query += f"{isResizable},"

        try:
            contestStartTime = contestDetails['contestStartTime']
        except KeyError:
            contestStartTime = 'NULL'
        if contestStartTime is None:
            contestStartTime = 'NULL'
            query += f"{contestStartTime}"
        else:
            contestStartTime = contestStartTime.replace('T', ' ')
            contestStartTime = contestStartTime.replace('Z', '')
            query += f"\'{contestStartTime}\',"

        try:
            gameTypeId = contestDetails['gameTypeId']
            if gameTypeId is None:
                gameTypeId = 'NULL'
        except KeyError:
            gameTypeId = 'NULL'
        query += f"{gameTypeId},"

        try:
            if contestDetails['ticketOnlyEntry'] == "true":
                ticketOnlyEntry = 1
            elif contestDetails['ticketOnlyEntry'] is None:
                ticketOnlyEntry = 'NULL'
            else:
                ticketOnlyEntry = 0
        except KeyError:
            ticketOnlyEntry = 'NULL'
        query += f"{ticketOnlyEntry},"

        try:
            name = contestDetails['name']
        except KeyError:
            name = 'NULL'
        if name is None:
            name = 'NULL'
            query += f"{name}"
        else:
            query += f"\'{name}\',"

        try:
            draftGroupId = contestDetails['draftGroupId']
            if draftGroupId is None:
                draftGroupId = 'NULL'
        except KeyError:
            draftGroupId = 'NULL'
        query += f"{draftGroupId},"

        try:
            playTypeId = contestDetails['playTypeId']
            if playTypeId is None:
                playTypeId = 'NULL'
        except KeyError:
            playTypeId = 'NULL'
        query += f"{playTypeId},"

        try:
            maximumEntries = contestDetails['maximumEntries']
            if maximumEntries is None:
                maximumEntries = 'NULL'
        except KeyError:
            maximumEntries = 'NULL'
        query += f"{maximumEntries},"

        try:
            maximumEntriesPerUser = contestDetails['maximumEntriesPerUser']
            if maximumEntriesPerUser is None:
                maximumEntriesPerUser = 'NULL'
        except KeyError:
            maximumEntriesPerUser = 'NULL'
        query += f"{maximumEntriesPerUser},"

        try:
            entryFee = contestDetails['entryFee']
            if entryFee is None:
                entryFee = 'NULL'
        except KeyError:
            entryFee = 'NULL'
        query += f"{entryFee},"

        try:
            crownAmount = contestDetails['crownAmount']
            if crownAmount is None:
                crownAmount = 'NULL'
        except KeyError:
            crownAmount = 'NULL'
        query += f"{crownAmount},"

        try:
            totalPayouts = contestDetails['totalPayouts']
            if totalPayouts is None:
                totalPayouts = 'NULL'
        except KeyError:
            totalPayouts = 'NULL'
        query += f"{totalPayouts},"

        query = query + f"{contestID})"

        try:
            cursor.execute(query)
        except Errors.DataError:
            print(query)
            return -1
        except Errors.ProgrammingError:
            print(query)
            return -1
