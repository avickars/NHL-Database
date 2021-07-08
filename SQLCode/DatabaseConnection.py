import mysql.connector


class sql_connection():
    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def open(self):
        self.conn = mysql.connector.connect(host=self.server, user=self.user, password=self.password, database=self.database)
        return self.conn

    def close(self):
        self.conn.close()


