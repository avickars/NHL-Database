from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import datetime


def create_daily_update_schedule():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    start = datetime.datetime(2021,7,11)
    for i in range(0,52):
        query = f"insert into weekly_update_schedule values (\"{start}\")"
        cursor.execute(query)
        connection.commit()
        start += datetime.timedelta(days=7)
    conn.close()


def main():
    create_daily_update_schedule()


if __name__ == '__main__':
    main()
