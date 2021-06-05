import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time
import pyodbc


def get_headshots():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current players (checking the live feed for new players)
    players = pd.read_sql_query("select distinct playerID from players", connection)

    for index, playerID in players.iterrows():
        playerID = playerID.values[0]
        headshotURL = f"\'https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{playerID}.jpg\'"

        query = f"insert into head_shots values ({playerID}, {headshotURL}, \'{get_time()}\')"

        try:
            cursor.execute(query)
            connection.commit()
        except pyodbc.DataError:
            print("ERROR")
            print(query)
            return -1
        except pyodbc.ProgrammingError:
            print("ERROR")
            print(query)
            return -1
