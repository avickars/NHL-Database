import mysql.connector
from MySQLCode import DatabaseCredentials as DBC

credentials = DBC.DataBaseCredentials()


def mysql_open():
    connection = mysql.connector.connect(
        host=credentials.host,
        user=credentials.user,
        password=credentials.password,
        database='hockey',
        auth_plugin='mysql_native_password'
    )
    return connection


def mysql_close(connection):
    connection.close()
