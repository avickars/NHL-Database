import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from DataGenerators.get_time import get_time
import pyodbc


def get_trophy_winners():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the current winners
    winners = pd.read_sql_query("select * from trophy_winners", connection)

    trophies = pd.read_sql_query("select trophyID from trophies", connection)

    for index, trophy in trophies.iterrows():
        trophyID = trophy.values[0]
        print(trophyID)

        url = requests.get(f"https://records.nhl.com/site/api/award-details?cayenneExp=trophyId={trophyID}")
        url_data = url.json()
        for winner in url_data['data']:
            trophyID = winner['trophyId']
            seasonID = winner['seasonId']

            coachID = winner['coachId']
            if coachID is None:
                coachID = -1

            playerID = winner['playerId']
            if playerID is None:
                playerID = -1

            fullName = winner['fullName']
            if fullName is None:
                fullName = f"\'N/A\'"
            else:
                fullName = fullName.replace("\'", " ")
                fullName = f"\'{fullName}\'"

            # Testing to see if we already have the winner in the system
            if len(winners[(winners['trophyID'] == trophyID) &
                           (winners['seasonID'] == seasonID) &
                           (winners['playerID'] == playerID) &
                           (winners['coachID'] == coachID) &
                           (winners['fullName'] == fullName.replace("\'",""))]) == 0:

                awardedPosthumously = winner['awardedPosthumously']
                if awardedPosthumously == True:
                    awardedPosthumously = 1
                else:
                    awardedPosthumously = 0

                isRookie = winner['isRookie']
                if isRookie == True:
                    isRookie = 1
                else:
                    isRookie = 0

                status = f"\'{winner['status']}\'"

                teamID = winner['teamId']
                if teamID is None:
                    teamID = 'NULL'

                voteCount = winner['voteCount']
                if voteCount is None:
                    voteCount = 'NULL'

                imageURL = winner['imageUrl']
                if imageURL is None:
                    imageURL = 'NULL'
                else:
                    imageURL = f"\'{imageURL}\'"



                query = f"insert into trophy_winners values ({awardedPosthumously}, {coachID}, {isRookie}, {playerID}, {seasonID}, {status}, {teamID}, {trophyID}, {voteCount}, {imageURL}, {fullName})"
                try:
                    cursor.execute(query)
                    cursor.commit()
                except pyodbc.IntegrityError:
                    print(query)
                    return -1
                except pyodbc.ProgrammingError:
                    print(query)
                    return -1
            else:
                continue

    conn.close()
    return 0
