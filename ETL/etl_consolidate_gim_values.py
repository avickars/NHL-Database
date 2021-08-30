import pandas as pd
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import numpy as np
import datetime
from datetime import date


def get_new_consolidated_gims():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'get_new_consolidated_gims' order by date desc limit 1",
                                      connection)

    # If we've never run it before, we start from the beginning
    if len(mostRecentRun) == 0:
        date_time_str = '2000-10-04 01:55:19'
        mostRecentRun = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        mostRecentRun = mostRecentRun.date()
    else:
        # Otherwise just converting it into sql form
        # Converting it from np.datetime64 to datetime
        # CITATION: https://stackoverflow.com/questions/13703720/converting-between-datetime-timestamp-and-datetime64
        mostRecentRun = (mostRecentRun['date'].values[0] - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        mostRecentRun = datetime.datetime.utcfromtimestamp(mostRecentRun)  # Adding one day on since we already ran it
        mostRecentRun = mostRecentRun.date()

    # Getting all the games we need to get the live data for (i.e. everything from our last run up to games played yesterday)
    minGameID = pd.read_sql_query(f"select min(gameID) from schedules where gameDate >= '{mostRecentRun}' and gameDate <'{date.today()}'", connection).values[0][0]

    # There are no games to do
    if minGameID == None:
        return 0

    # Getting the season mapping
    SEASON_MAPPING = pd.read_sql_query("""
    select * from season_to_next_season_mapping
    """, connection)

    # Getting the current season
    cursor.execute("select max(seasonID) from seasons")
    CURRENT_SEASON = cursor.fetchall()[0][0]

    # Getting the previous_Season
    PREVIOUS_SEASON = SEASON_MAPPING[SEASON_MAPPING['seasonID'] == CURRENT_SEASON]['previousSeasonID'].values[0]

    # Getting the GIM values for all games since last run
    GIM_VALUES = pd.read_sql_query(f"""
    select *
    from (
             select GAMES.seasonID,
                    GAMES.gameID,
                    GAMES.gameType,
                    GAMES.teamID,
                    GAMES.playerID,
                    IF(GIM.value is null, 0, GIM.value)                                                                               as 'gimForIndvGame',
                    ROW_NUMBER() over (partition by GAMES.seasonID, GAMES.playerID order by GAMES.gameID)                             as 'gameNumber',
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
                      where scratched = 0
                        and seasonID >= 20102011
                        and timeOnIce is not null
                        and s.gameType in ('R', 'P')
                  ) GAMES
                      left join
                  (
                      select gim.gameID,
                             playerID,
                             sum(if(awayTeam = 1, awayProbability, homeProbability)) as 'value'
                      from stage_hockey.gim_values gim
                      group by gim.gameID, playerID
                  ) GIM ON GAMES.gameID = GIM.gameID and GAMES.playerID = GIM.playerID
             where GAMES.seasonID >= {CURRENT_SEASON}
             order by gameID, playerID
         ) p where gameID >= {minGameID}
    """, connection)

    # Getting each players position
    POSITIONS = pd.read_sql_query("""
    select playerID,
                 primaryPositionCode,
                 row_number() over (partition by playerID order by date desc ) as 'ROW_NUM'
          from plays_position
          where primaryPositionCode is not null
    """, connection)
    POSITIONS = POSITIONS[POSITIONS['ROW_NUM'] == 1].drop(['ROW_NUM'], axis=1)

    # Getting last seasons positional average
    POSITIONS_AVERAGES = pd.read_sql_query(f"""
    select * from stage_hockey.gim_position_averages_per_season where seasonID = {PREVIOUS_SEASON}
    """, connection)

    # Getting each players GIM for last season
    pastGIMValues = pd.read_sql_query(f"""
    select * from stage_hockey.gim_by_player_by_season where seasonID = {PREVIOUS_SEASON}
    """, connection)

    # Joining the season mapping to add on the previous season
    gimValuesAdjusted = pd.merge(GIM_VALUES,
                                 SEASON_MAPPING,
                                 how='inner', on=['seasonID'])

    # Joining on each players gim values last season
    gimValuesAdjusted = pd.merge(gimValuesAdjusted,
                                 pastGIMValues,
                                 how='left',
                                 left_on=['previousSeasonID', 'playerID'],
                                 right_on=['seasonID', 'playerID'],
                                 suffixes=('', '_previous')).drop(['seasonID_previous'], axis=1)

    # Adding on the position each player plays
    gimValuesAdjusted = pd.merge(gimValuesAdjusted, POSITIONS, how='inner')

    # Adding on the positional averages from last season
    gimValuesAdjusted = pd.merge(gimValuesAdjusted, POSITIONS_AVERAGES, how='inner',
                                 left_on=['previousSeasonID', 'primaryPositionCode'],
                                 right_on=['seasonID', 'primaryPositionCode'],
                                 suffixes=('', '_positionalMean')).drop(['primaryPositionCode'], axis=1)

    """
    LOGIC: 
        - if player has played 20 or more games this season, then we just use their gimMean
        - if a player didn't play last year, then we use the positional average from last year in combination with their current GIM mean
        - if a player has played less than 20 games, then we use their GIM from last season with their current GIM mean 
    """
    gimValuesAdjusted['gimMeanAdjusted'] = np.where(gimValuesAdjusted['gameNumber'] >= 20,
                                                    gimValuesAdjusted['gimMean'],
                                                    np.where(gimValuesAdjusted['gimValueAdjusted'].isna(),
                                                             (gimValuesAdjusted['gameNumber'] / 20) * gimValuesAdjusted['gimMean'] + (1 - gimValuesAdjusted['gameNumber'] / 20) * gimValuesAdjusted[
                                                                 'gimMean_positionalMean'],
                                                             (gimValuesAdjusted['gameNumber'] / 20) * gimValuesAdjusted['gimMean'] + (1 - gimValuesAdjusted['gameNumber'] / 20) * gimValuesAdjusted[
                                                                 'gimValueAdjusted']))

    # Dropping columns
    gimValuesAdjusted = gimValuesAdjusted.drop(['previousSeasonID',
                                                'gimValueAdjusted',
                                                'seasonID_positionalMean',
                                                'gimMean_positionalMean'], axis=1)

    for index, row in gimValuesAdjusted.iterrows():
        query = f"insert into stage_hockey.gim_values_consolidated values({row['seasonID']},{row['gameID']},\'{row['gameType']}\',{row['teamID']},{row['playerID']},{row['gimForIndvGame']},{row['gameNumber']},{row['gimCumTotal']},{row['gimMean']},{row['gimMeanAdjusted']})"
        cursor.execute(query)
        connection.commit()

    conn.close()
