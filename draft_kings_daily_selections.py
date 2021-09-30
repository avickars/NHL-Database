from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from datetime import datetime
from DraftKings.contest_selections_generators import get_selections
import heapq
from pytz import timezone
import time


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    contests = pd.read_sql_query(
        f"select contestID from draft_kings.contest_details where contestStartTime >= CONVERT_TZ(\'{datetime.today().date()} 0:00:00\','right/US/Pacific','UTC') and contestStartTime <= CONVERT_TZ(\'{datetime.today().date()} 23:59:59\','right/US/Pacific','UTC')",
        connection)
    # contests = pd.read_sql_query(f"# select contestID, contestStartTime from draft_kings.contest_details", connection)

    # Defining the heap to hold the contests
    contestHeap = []

    for index, contest in contests.iterrows():
        # Pushing the contests onto the heap (key is the start time)
        heapq.heappush(contestHeap, (contest['contestStartTime'], contest['contestID']))

    while len(contestHeap) > 0:
        # Getting the current time
        nowTime = datetime.now(timezone('UTC')).replace(tzinfo=None)

        # Getting the time of the next contest
        nextContestTime = contestHeap[0][0]

        # Getting the number of seconds between now and the next contest
        difference = (nextContestTime - nowTime).total_seconds()

        # If the contest is currently happening
        if difference <= -60:
            contestTime, contestID = heapq.heappop(contestHeap)
            if get_selections(cursor, connection, contestID) == -1:
                conn.close()
                return -1
            connection.commit()
        # Otherwise its not, so we'll go to sleep until it happens
        else:
            time.sleep(difference + 60)

    conn.close()


if __name__ == '__main__':
    main()
