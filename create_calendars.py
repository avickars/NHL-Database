import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
import datetime
from random import randint


def create_daily_update_calendar(cursor):
    start = datetime.date(2021, 6, 7)
    while start <= datetime.date(2022, 6, 7):
        query = f"insert into daily_update_schedule values (\'{start}\')"
        cursor.execute(query)
        cursor.commit()
        start += datetime.timedelta(days=1)

def create_weekly_update_calendar(cursor):
    start = datetime.date(2021, 6, 13)
    while start <= datetime.date(2022, 6, 13):
        query = f"insert into weekly_update_schedule values (\'{start}\')"
        cursor.execute(query)
        cursor.commit()
        start += datetime.timedelta(weeks=1)


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # create_daily_update_calendar(cursor)
    create_weekly_update_calendar(cursor)

    conn.close()


if __name__ == '__main__':
    main()
