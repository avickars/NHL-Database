from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import datetime


def create_daily_update_schedule():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    for i in range(0,800):
        query = f"insert into daily_update_schedule values (\"{datetime.date.today() + datetime.timedelta(days=i)}\")"
        cursor.execute(query)
        connection.commit()
    conn.close()


def main():
    create_daily_update_schedule()


if __name__ == '__main__':
    main()
