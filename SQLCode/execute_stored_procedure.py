from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC

def execute_proc(proc):
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # From Raw to Stage
    query = f"call {proc}();"
    cursor.execute(query)
    connection.commit()

    conn.close()