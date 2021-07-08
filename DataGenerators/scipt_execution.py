from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.get_time import get_time


def record_script_execution(script):
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    query = f"insert into script_execution values (\'{script}\', \'{get_time()}\')"
    cursor.execute(query)
    connection.commit()

    conn.close()
