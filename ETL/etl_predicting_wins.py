from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import datetime
import pandas as pd
import numpy as np


def predict_wins():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()

    # Getting the most recent run
    mostRecentRun = pd.read_sql_query("select date from script_execution where script = 'predict_wins' order by date desc limit 1",
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

    print(mostRecentRun)
