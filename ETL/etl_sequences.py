from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import datetime
import pandas as pd
import numpy as np
from datetime import date
from sklearn.feature_extraction.text import CountVectorizer


def create_gim_model_input():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'create_gim_model_input' order by date desc limit 1",
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
    print('Loading Data')
    rawDataFiltered = pd.read_sql_query(f"""
                                    select lf.eventID,
                                           s.gameID,
                                           IF(lf.eventTypeID = 'GOAL' and lf.playerType = 'Assist', 'Assist', lf.eventTypeID) as 'eventTypeID',
                                           lf.playerType,
                                           lf.eventDescription,
                                           lf.periodNum,
                                           lf.periodTime,
                                           lf.xCoordinate,
                                           lf.yCoordinate,
                                           lf.teamID,
                                           s.homeTeamID,
                                           s.awayTeamID,
                                           lf.playerID,
                                           lf.penaltyMinutes,
                                           bs.teamID as 'teamID_box'
                                    from live_feed lf
                                        inner join schedules s on lf.gameID = s.gameID
                                        left join box_scores bs on lf.gameID = bs.gameID and lf.playerID = bs.playerID
                                    where gameDate >= '{mostRecentRun}' and
                                          seasonID>=20102011 and
                                          gameType = 'R'  and
                                          (eventSubID = 0 or playerType = 'Assist') and
                                          eventTypeID in ('FACEOFF',
                                                          'SHOT',
                                                          'MISSED_SHOT',
                                                          'BLOCKED_SHOT',
                                                          'TAKEAWAY',
                                                          'GIVEAWAY',
                                                          'HIT',
                                                          'GOAL',
                                                          'ASSIST',
                                                          'PERIOD_END',
                                                          'EARLY_INT_START',
                                                          'PENALTY',
                                                          'STOP',
                                                          'EARLY_INT_END',
                                                          'EARLY_INT_END') and
                                          periodNum <= 3
                                    order by gameID ,eventID, eventSubID asc
                                """, connection)

    # Closing the connection as it is no longer needed
    connection.close()

    if len(rawDataFiltered) == 0:
        return 0

    # Getting the team type (home/away) for each event if possible
    rawDataFiltered['teamType'] = rawDataFiltered.apply(lambda row: team_type(row['teamID'],
                                                                              row['homeTeamID'],
                                                                              row['awayTeamID']), axis=1)

    # Normalizing the xCoordinate for both teams (offensive side is positive, defensive side is negative)
    rawDataFiltered['xCoordinate'] = rawDataFiltered.apply(lambda row: coordinate_normalization(row['xCoordinate'],
                                                                                                row['teamType'],
                                                                                                row['periodNum']), axis=1)

    # Converting the time to the number of seconds that have elapsed
    rawDataFiltered['secondsElapsed'] = rawDataFiltered.apply(lambda row: elapsed_seconds(row['periodNum'], row['periodTime']), axis=1)

    # Converting the raw data to sequences of actions
    sequenceData = create_sequence_data(rawDataFiltered)

    # Vectorizing the events
    eventVectorizer = CountVectorizer()
    eventVectorizer.fit(sequenceData['event'])
    vectorizedEvents = eventVectorizer.transform(sequenceData['event']).toarray()

    # List of actions in the correct order according to its position on the vectorized array
    actions = [action[0] for action in sorted(eventVectorizer.vocabulary_.items())]

    # Adding in the vectorized columns
    for action in range(0, len(actions)):
        sequenceData.insert(column=actions[action], value=vectorizedEvents[:, action], loc=len(sequenceData.columns))

    # Dropping event as it is no longer needed
    sequenceData = sequenceData.drop(['event'], axis=1)

    # Vectorizing the teams
    teamVectorizer = CountVectorizer()
    teamVectorizer.fit(sequenceData['team'])
    vectorizedTeams = teamVectorizer.transform(sequenceData['team']).toarray()

    # List of teams in the correct order according to its position on the vectorized array
    teams = [action[0] for action in sorted(teamVectorizer.vocabulary_.items())]

    # Adding in the vectorized columns
    for team in range(0, len(teams)):
        sequenceData.insert(column=teams[team], value=vectorizedTeams[:, team], loc=len(sequenceData.columns))

    # Dropping event as it is no longer needed
    sequenceData = sequenceData.drop(['team'], axis=1)

    # Ensuring we have constant columns (i.e. no NAs)
    for column in [ 'blocked_shot',
          'faceoff',
          'giveaway',
          'goal',
          'assist',
          'hit',
          'missed_shot',
          'penalty',
          'shot',
          'takeaway']:
        if column not in sequenceData.columns:
            sequenceData[column] = 0

    # All values should be ints, a couple of them ended up as floats for some reason.
    sequenceData = sequenceData.astype(int)

    # Opening new connection to dump the new data
    conn = DatabaseConnection.sql_connection(creds.server, 'stage_hockey', creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    for index, row in sequenceData.iterrows():
        query = convert_to_mysql_query('gim_sequences', row)
        cursor.execute(query)
        connection.commit()
    connection.close()


def convert_to_mysql_query(table, row):
    queryPart1 = f"insert into {table} ("
    queryPart2 = "values ("
    for index, item in row.items():
        queryPart1 += "" + index + ","
        queryPart2 += "" + str(item) + ","

    queryPart1 = queryPart1[0:-1] + ") "
    queryPart2 = queryPart2[0:-1] + ") "
    return queryPart1 + queryPart2


def create_sequence_data(rawDataFiltered):
    print('Creating Sequence Data')
    sequences = []
    actionEvents = ['FACEOFF',
                    'SHOT',
                    'MISSED_SHOT',
                    'BLOCKED_SHOT',
                    'TAKEAWAY',
                    'GIVEAWAY',
                    'HIT',
                    'ASSIST',
                    'GOAL']
    startEndEvents = ['PERIOD_START',
                      'PERIOD_END',
                      'EARLY_INT_START',
                      'PENALTY',
                      'STOP',
                      'SHOOTOUT_COMPLETE',
                      'GAME_END',
                      'EARLY_INT_END',
                      'EARLY_INT_END']

    sequenceNum = 0
    eventNum = 0
    penaltyQueue = Queue()
    gameID = 0
    context = {'goalDiff': 0, 'manpowerDiff': 0, 'periodNum': 1}
    for index, row in rawDataFiltered.iterrows():
        if index % 100000 == 0:
            print((index / len(rawDataFiltered)) * 100, '%')

        # Resetting the context
        if gameID != row['gameID']:
            gameID = row['gameID']
            context = {'goalDiff': 0, 'manpowerDiff': 0, 'periodNum': 1}

        # Updating the context if needed
        if row['periodNum'] != context['periodNum']:
            context['periodNum'] = row['periodNum']

        # Computing if respective team is home or away
        teamType = team_type(row['teamID'], row['homeTeamID'], row['awayTeamID'])

        # If there currently is a penalty in the penalty queue
        if penaltyQueue.size() > 0:
            # Determining the time of the action
            actionTime = elapsed_seconds(row['periodNum'], row['periodTime'])

            # Iterating through all  the penalties in the queue from oldest to newest
            for penalty in reversed(penaltyQueue.get_queue()):
                # If the action occured after the penalty ended, we update the context and pop the penalty
                if penalty['penaltyEnd'] < actionTime:
                    # Popping the penalty
                    penaltyQueue.remove(penalty)

                    # Updating the context
                    if penalty['team'] == 'HOME':
                        context['manpowerDiff'] -= 1
                    else:
                        context['manpowerDiff'] -= -1

        # Catching penalties to update the context
        if row['eventTypeID'] == 'PENALTY':
            if int(row['penaltyMinutes']) != 10:
                # Getting the end time of the penalty (in seconds)
                penaltyStart = elapsed_seconds(row['periodNum'], row['periodTime'])
                penaltyEnd = penaltyStart + row['penaltyMinutes'] * 60

                # Determining who took the penalty to update the context
                if teamType == 'HOME':
                    context['manpowerDiff'] += 1
                else:
                    context['manpowerDiff'] += -1

                # Enqueuing the penalty
                penaltyQueue.enqueue({'team': teamType,
                                      'penaltyStart': penaltyStart,
                                      'penaltyEnd': penaltyEnd,
                                      'penaltyLength':
                                          row['penaltyMinutes']})

        # Adding in the event if it is a goal or assist (doing it here in since the context will be updated below)
        if (row['eventTypeID'] == 'ASSIST'):
            sequences.append([row['gameID'],
                              context['goalDiff'],
                              context['manpowerDiff'],
                              context['periodNum'],
                              sequenceNum,
                              eventNum,
                              row['eventTypeID'],  # action type
                              teamType,  # Home/Away
                              row['secondsElapsed'],
                              row['xCoordinate'],
                              row['yCoordinate'],
                              row['playerID']])  # Neutral/Offensive/Defensive/NULL

        # If the event type is a goal
        if row['eventTypeID'] == 'GOAL':
            # Injecting the shot before the goal# Adding in the next sequency
            sequences.append([row['gameID'],
                              context['goalDiff'],
                              context['manpowerDiff'],
                              context['periodNum'],
                              sequenceNum,
                              eventNum,
                              'SHOT',  # action type
                              teamType,  # Home/Away
                              #                       row['zone']
                              row['secondsElapsed'],
                              row['xCoordinate'],
                              row['yCoordinate'],
                              row['playerID']])  # Neutral/Offensive/Defensive/NULL
            # Incrementing the event number
            eventNum += 1

            # Adding in the goal
            sequences.append([row['gameID'],
                              context['goalDiff'],
                              context['manpowerDiff'],
                              context['periodNum'],
                              sequenceNum,
                              eventNum,
                              row['eventTypeID'],  # action type
                              teamType,  # Home/Away
                              row['secondsElapsed'],
                              row['xCoordinate'],
                              row['yCoordinate'],
                              row['playerID']])  # Neutral/Offensive/Defensive/NULL

            # Updating the context
            if teamType == 'HOME':
                context['goalDiff'] -= 1
            else:
                context['goalDiff'] += 1

            # Defining home/away flags to only pop off the minimum number of penalties
            FLAGS = {'HOME': True, 'AWAY': True}

            # Determining the time of the action
            actionTime = elapsed_seconds(row['periodNum'], row['periodTime'])

            # If there currently is a penalty in the penalty queue
            if penaltyQueue.size() > 0:

                # Iterating through all  the penalties in the queue from oldest to newest
                for penalty in reversed(penaltyQueue.get_queue()):

                    # If the penalty is a 5 minute major, the player must serve the full 5 minutes (no change needed)
                    # If the penalty is over it would have been popped in the above if statement
                    if penalty['penaltyLength'] == 5:
                        continue
                    else:

                        # Making sure its not a shorthanded goal and we haven't already popped a penalty for this goal/team
                        if (penalty['team'] != teamType) & (FLAGS[penalty['team']]):

                            # Creating the updated penalty
                            newPenalty = penalty
                            newPenalty['penaltyStart'] = actionTime
                            newPenalty['penaltyLength'] += -120
                            newPenalty['penaltyEnd'] = newPenalty['penaltyStart'] + newPenalty['penaltyLength']

                            if penalty['penaltyLength'] <= 0:

                                # Popping the penalty off
                                penaltyQueue.remove(penalty)

                                # Updating the context
                                if penalty['team'] == 'HOME':
                                    context['manpowerDiff'] -= 1
                                else:
                                    context['manpowerDiff'] -= -1
                            else:

                                # replacing the old penalty info with the new one
                                penaltyQueue.exchange(penalty, newPenalty)

                            FLAGS[penalty['team']] = False

                            #     # Updating the context if needed
        #     if row['periodNum'] != context['periodNum']:
        #         context['periodNum'] = row['periodNum']

        # Adding in the next sequency
        if (((row['eventTypeID'] not in startEndEvents) |
             (row['eventTypeID'] == 'PENALTY')) &
                (row['eventTypeID'] != 'GOAL') &
                (row['eventTypeID'] != 'ASSIST')):
            sequences.append([row['gameID'],
                              context['goalDiff'],
                              context['manpowerDiff'],
                              context['periodNum'],
                              sequenceNum,
                              eventNum,
                              row['eventTypeID'],  # action type
                              teamType,  # Home/Away
                              row['secondsElapsed'],
                              row['xCoordinate'],
                              row['yCoordinate'],
                              row['playerID']])  # Neutral/Offensive/Defensive/NULL
        if row['eventTypeID'] in actionEvents:
            eventNum += 1
        else:
            sequenceNum += 1
            eventNum = 0
    #     break
    sequenceData = pd.DataFrame(sequences,
                                columns=['gameID',
                                         'goalDiff',
                                         'manpowerDiff',
                                         'periodNum',
                                         'sequenceNum',
                                         'eventNum',
                                         'event',
                                         'team',
                                         'secondsElapsed',
                                         'xCoord',
                                         'yCoord',
                                         'playerID'])

    # Removing any rows that contain a null value
    sequenceData = sequenceData[~sequenceData['sequenceNum'].isin(sequenceData[sequenceData.isnull().any(axis=1)]['sequenceNum'].values)]

    return sequenceData


def team_type(teamID, homeTeamID, awayTeamID):
    if teamID == homeTeamID:
        return 'HOME'
    elif teamID == awayTeamID:
        return 'AWAY'
    else:
        return np.nan


def coordinate_normalization(xCoord, teamType, periodNum):
    if teamType == np.nan:
        return None
    else:
        if int(periodNum) % 2 == 1:
            if teamType == 'AWAY':
                return xCoord
            else:
                return -1 * xCoord
        else:
            if teamType == 'AWAY':
                return -1 * xCoord
            else:
                return xCoord


def elapsed_seconds(periodNum, periodTime):
    periodTime = pd.Timedelta(periodTime)
    return (int(periodNum) - 1) * 20 * 60 + periodTime.total_seconds() / 60


class Queue:
    # CITATION: https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaQueueinPython.html
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return self.queue == []

    def enqueue(self, item):
        self.queue.insert(0, item)

    def dequeue(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)

    def get_queue(self):
        return self.queue

    def exchange(self, oldItem, newItem):
        self.queue[self.queue.index(oldItem)] = newItem

    def remove(self, item):
        self.queue.remove(item)


