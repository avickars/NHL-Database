import requests
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC


def get_logos():
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    query = f"truncate table team_logos;"
    cursor.execute(query)
    connection.commit()

    url_string = "https://records.nhl.com/site/api/franchise?include=teams.id&include=teams.active&include=teams.triCode&include=teams.placeName&include=teams.commonName&include=teams.fullName&include=teams.logos&include=teams.conference.name&include=teams.division.name&include=teams.franchiseTeam.firstSeason.id&include=teams.franchiseTeam.lastSeason.id&include=teams.franchiseTeam.teamCommonName"
    url = requests.get(url_string)
    url_data = url.json()
    data = url_data['data']
    for franchise in data:
        franchiseID = franchise['id']
        for team in franchise['teams']:
            teamID = team['id']
            for logo in team['logos']:
                startSeason = logo['startSeason']
                endSeason = logo['endSeason']
                logoURL = logo['url']
                logoID = logo['id']

                background = logo['background']

                query = f"insert into team_logos values ({franchiseID}, {teamID},{startSeason},{endSeason},{logoID}, \"{logoURL}\", \"{background}\")"
                cursor.execute(query)
                connection.commit()