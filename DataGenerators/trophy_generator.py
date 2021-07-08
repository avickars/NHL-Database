import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time


def get_trophies():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current conferences
    trophies = pd.read_sql_query("select * from trophies", connection)


    # Getting trophy information
    url = requests.get(f"https://records.nhl.com/site/api/trophy")
    url_data = url.json()
    for trophy in url_data['data']:
        trophyID = trophy['id']

        # Testing to see if we already have the trophy in the system
        if len(trophies[trophies['trophyID'] == trophyID]) == 0:
            categoryID = trophy['categoryId']

            description = trophy['briefDescription']

            imageURL = trophy['imageUrl']

            name = trophy['name']

            shortName = trophy['shortName']

            query = f"insert into trophies values ({trophyID}, {categoryID}, \'{description}\', \'{imageURL}\', \'{name}\', \'{shortName}\')"
            cursor.execute(query)
            connection.commit()
        else:
            continue

    conn.close()
    return 0
