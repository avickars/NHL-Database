from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC

creds = DBC.DataBaseCredentials()
conn = DatabaseConnection.sql_connection('homeserver', 'hockey', creds.user, creds.password)

conn = conn.open()

conn.execute('select * from prospectCategory')

row = conn.fetchone()
while row:
    print(row)
    row = conn.fetchone()


