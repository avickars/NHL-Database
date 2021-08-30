import pandas as pd
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import numpy as np


def gim_yearly_update():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the season mappings
    SEASON_MAPPING = pd.read_sql_query("""
    select * from season_to_next_season_mapping
    """, connection)

    # Getting the current season
    cursor.execute("select max(seasonID) from seasons")
    CURRENT_SEASON = cursor.fetchall()[0][0]
    print(SEASON_MAPPING[SEASON_MAPPING['seasonID'] == CURRENT_SEASON]['previousSeasonID'])

    # Getting the previous_Season
    PREVIOUS_SEASON = SEASON_MAPPING[SEASON_MAPPING['seasonID'] == CURRENT_SEASON]['previousSeasonID'].values[0]

    # Selecting GIM for this and last season
    GIM_VALUES = pd.read_sql_query(f"""
    select GAMES.seasonID,
           GAMES.gameID,
           GAMES.gameType,
           GAMES.teamID,
           GAMES.playerID,
           IF(GIM.value is null, 0, GIM.value) as 'gimForIndvGame',
           ROW_NUMBER() over (partition by GAMES.seasonID, GAMES.playerID order by GAMES.gameID) as 'gameNumber',
           SUM(IF(GIM.value is null, 0, GIM.value)) over (partition by GAMES.seasonID, GAMES.playerID order by GAMES.gameID) as 'gimCumTotal',
           AVG(IF(GIM.value is null, 0, GIM.value)) over (partition by GAMES.seasonID, GAMES.playerID order by GAMES.gameID) as 'gimMean'
    from (
             select s.seasonID,
                    bs.gameID,
                    bs.playerID,
                    bs.teamID,
                    s.gameType
             from box_scores bs
                      inner join schedules s on bs.gameID = s.gameID
             where scratched = 0 and
                   seasonID >= 20102011 and
                   timeOnIce is not null and
                   s.gameType in ('R', 'P')
         ) GAMES
    left join
        (
            select gim.gameID,
                   playerID,
                   sum(if(awayTeam = 1, awayProbability, homeProbability)) as 'value'
            from stage_hockey.gim_values gim
            group by gim.gameID, playerID
        ) GIM ON GAMES.gameID =  GIM.gameID and GAMES.playerID = GIM.playerID
    where GAMES.seasonID >= {PREVIOUS_SEASON}
    order by gameID,playerID;
    """, connection)

    GIM_BY_PLAYER_BY_SEASON, POSITIONS_AVERAGES, POSITIONS = update_gim_values_by_position(GIM_VALUES, cursor, connection, CURRENT_SEASON)
    update_gim_values_last_season(cursor, connection, GIM_BY_PLAYER_BY_SEASON, SEASON_MAPPING, POSITIONS, POSITIONS_AVERAGES)

    conn.close()


def update_gim_values_last_season(cursor, connection, GIM_BY_PLAYER_BY_SEASON, SEASON_MAPPING, POSITIONS, POSITIONS_AVERAGES):
    # Taking this seasons current season and determining the past season
    pastGIMValues = pd.merge(GIM_BY_PLAYER_BY_SEASON,
                             SEASON_MAPPING,
                             how='inner',
                             left_on=['seasonID'],
                             right_on=['seasonID'])

    # Adding on their GIM values for last season
    pastGIMValues = pd.merge(pastGIMValues,
                             GIM_BY_PLAYER_BY_SEASON,
                             how='left',
                             left_on=['previousSeasonID', 'playerID'],
                             right_on=['seasonID', 'playerID'],
                             suffixes=('', '_previous'))

    # Getting their positions
    pastGIMValues = pd.merge(pastGIMValues, POSITIONS, how='inner')

    # Don't need this column anymore
    pastGIMValues = pastGIMValues.drop(['seasonID_previous'], axis=1)

    # Getting last seasons position averages
    pastGIMValues = pd.merge(pastGIMValues,
                             POSITIONS_AVERAGES,
                             how='inner',
                             left_on=['previousSeasonID', 'primaryPositionCode'],
                             right_on=['seasonID', 'primaryPositionCode'],
                             suffixes=('', '_positionalMean'))

    # Don't need this column anymore
    pastGIMValues = pastGIMValues.drop('seasonID_positionalMean', axis=1)

    """
    LOGIC:
        - if the player played no games in the previous year, we just take the position mean of the previous season
        - if the player played more than 20 games, we just take the previous years value
        - if the player played less than 20 games then we use the position position mean with last seasons positional mean
    """
    gimValuesMinus2Years = np.where(pastGIMValues['gameNumber_previous'].isna(),
                                    pastGIMValues['gimMean_positionalMean'],
                                    np.where(pastGIMValues['gameNumber_previous'] >= 20,
                                             pastGIMValues['gimMean_previous'],
                                             (pastGIMValues['gameNumber_previous'] / 20) * pastGIMValues['gimMean_previous'] + (1 - pastGIMValues['gameNumber_previous'] / 20) * pastGIMValues[
                                                 'gimMean_positionalMean']))

    """
    LOGIC:
        Basically the same as above
    """
    gimValues = np.where(pastGIMValues['gameNumber'] >= 20,
                         pastGIMValues['gimMean'],
                         (pastGIMValues['gameNumber'] / 20) * pastGIMValues['gimMean'] + (1 - pastGIMValues['gameNumber'] / 20) * gimValuesMinus2Years)

    # Only getting what we need
    pastGIMValues = pastGIMValues[['seasonID', 'playerID']]

    # Getting the adjusted values
    pastGIMValues['gimValueAdjusted'] = gimValues

    for index, row in pastGIMValues.iterrows():
        if index % 100 == 0:
            print((index / len(pastGIMValues)) * 100)
        query = f"insert into stage_hockey.gim_by_player_by_season values({row['seasonID']},{row['playerID']},{row['gimValueAdjusted']})"
        cursor.execute(query)
        connection.commit()


def update_gim_values_by_position(GIM_VALUES, cursor, connection, CURRENT_SEASON):
    # getting each players final gim for the regular season
    GIM_BY_PLAYER_BY_SEASON = pd.merge(GIM_VALUES[['seasonID', 'playerID', 'gameNumber', 'gimMean']],
                                       GIM_VALUES[GIM_VALUES['gameType'] == 'R'][['seasonID', 'playerID', 'gameNumber']].groupby(['seasonID', 'playerID']).max('gameNumber').reset_index(),
                                       how='inner',
                                       on=['seasonID', 'playerID', 'gameNumber'])

    # Getting each players position
    POSITIONS = pd.read_sql_query("""
    select playerID,
                 primaryPositionCode,
                 row_number() over (partition by playerID order by date desc ) as 'ROW_NUM'
          from plays_position
          where primaryPositionCode is not null
    """, connection)

    # Making sure we are using the most recent position info
    POSITIONS = POSITIONS[POSITIONS['ROW_NUM'] == 1].drop(['ROW_NUM'], axis=1)

    # Getting merging GIM to positions
    POSITIONS_AVERAGES = pd.merge(GIM_VALUES[['seasonID', 'playerID', 'gimMean']], POSITIONS, how='inner')

    # Getting the averages for eac position/season
    POSITIONS_AVERAGES = POSITIONS_AVERAGES.drop('playerID', axis=1).groupby(['seasonID', 'primaryPositionCode']).mean('gimMean').reset_index()

    # Inserting this seasons position averages into the table
    for index, row in POSITIONS_AVERAGES[POSITIONS_AVERAGES['seasonID'] == CURRENT_SEASON].iterrows():
        if index % 1000 == 0:
            print((index / len(POSITIONS_AVERAGES)) * 100)
        query = f"insert into stage_hockey.gim_position_averages_per_season values({row['seasonID']},\'{row['primaryPositionCode']}\',{row['gimMean']})"
        cursor.execute(query)
        connection.commit()

    return GIM_BY_PLAYER_BY_SEASON, POSITIONS_AVERAGES, POSITIONS
