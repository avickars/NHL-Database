import pyodbc


class sql_connection():
    def __init__(self, serverName, database, user, password):
        self.serverName = serverName
        self.database = database
        self.user = user
        self.password = password

    def open(self):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.serverName+';DATABASE='+self.database+';UID='+self.user+';PWD='+ self.password)
        self.conn = conn
        return conn

    def close(self):
        del  self.conn


