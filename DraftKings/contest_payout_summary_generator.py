import requests
import mysql.connector.errors as Errors



def get_payout_summary(cursor, contests):
    for contestID in contests:
        # url_string = f"https://api.draftkings.com/contests/v1/contests/114420180?format=json"
        url_string = f"https://api.draftkings.com/contests/v1/contests/{contestID}?format=json"
        url = requests.get(url_string)
        url_data = url.json()
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