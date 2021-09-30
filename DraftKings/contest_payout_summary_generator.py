import requests
import mysql.connector.errors as Errors
from DraftKings.timezone_conversion import timezone_converter
from datetime import datetime
from dateutil import parser


def get_payout_summary(cursor, contests):
    # Used in the contestStartTime section, defining it up here so as not to get redefined
    date_format = '%Y-%M-%d %H:%M:%S'

    for contestID in contests:
        url_string = f"https://api.draftkings.com/contests/v1/contests/{contestID}?format=json"
        url = requests.get(url_string)
        url_data = url.json()

        # Making sure to skip any contests that aren't today
        try:
            contestStartTime = url_data['contestDetail']['contestStartTime']
        except KeyError:
            contestStartTime = 'NULL'
        if contestStartTime is None:
            # just continuing since it'll break code down the line otherwise if I don't know when the contest starts
            continue
        else:
            contestStartTime = parser.parse(contestStartTime)
            if timezone_converter(contestStartTime).date() != datetime.today().date():
                continue


        payoutSummary = url_data['contestDetail']['payoutSummary']

        for payout in payoutSummary:
            query = "insert into draft_kings.contest_payouts values ("
            try:
                if payout['minPosition'] is not None:
                    minPosition = payout['minPosition']
                else:
                    minPosition = 'NULL'
            except KeyError:
                minPosition = 'NULL'
            query += f"{minPosition},"

            try:
                if payout['maxPosition'] is not None:
                    maxPosition = payout['maxPosition']
                else:
                    maxPosition = 'NULL'
            except KeyError:
                maxPosition = 'NULL'
            query += f"{maxPosition},"

            try:
                if payout['tierPayoutDescriptions']['Cash'] is not None:
                    Cash = payout['tierPayoutDescriptions']['Cash']
                    Cash = str(Cash).replace('$', '').replace(',', '')
                    Cash = float(Cash)
                else:
                    Cash = 'NULL'
            except KeyError:
                Cash = 'NULL'
            query += f"{Cash},"

            query += f"{contestID})"

            try:
                cursor.execute(query)
            except Errors.DataError:
                print(query)
                return -1
            except Errors.ProgrammingError:
                print(query)
                return -1
