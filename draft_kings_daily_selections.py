from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from datetime import datetime
from pytz import timezone
import pytz
from DraftKings.contest_selections_generator import get_selections
import heapq
from pytz import timezone
import time
from DraftKings.DraftKingsCredentials import DraftKingsCredentialsCredentials
import selenium.common.exceptions as execeptions
import socket
from selenium import webdriver
from DraftKings.draft_kings_script_execution import record_script_execution
from selenium.webdriver.chrome.options import Options


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    contests = pd.read_sql_query(
        f"""select max(cgt.startTime) as 'contestStartTime', CD.contestID
            from draft_kings.contest_details CD
            inner join draft_kings.contest_game_times cgt on CD.draftGroupId = cgt.draftGroupId
            where CD.contestStartTime >= CONVERT_TZ(\'{datetime.today().date()} 0:00:00\','right/US/Pacific','UTC') and 
                    CD.contestStartTime <= CONVERT_TZ(\'{datetime.today().date()} 23:59:59\','right/US/Pacific','UTC')
            group by CD.contestID""",
        connection)

    # Defining the heap to hold the contests
    contestHeap = []
    # get_selections(cursor, connection, 114697699)

    for index, contest in contests.iterrows():
        # Pushing the contests onto the heap (key is the start time)
        heapq.heappush(contestHeap, (contest['contestStartTime'], contest['contestID']))

    creds = DraftKingsCredentialsCredentials()
    browser = None

    while len(contestHeap) > 0:
        # Getting the current time
        nowTime = datetime.now(timezone('UTC')).replace(tzinfo=None)

        # Getting the time of the next contest
        nextContestTime = contestHeap[0][0]

        # Getting the number of seconds between now and the next contest
        difference = (nextContestTime - nowTime).total_seconds()

        # If the contest is currently happening
        if difference <= -60:
            print('ContestID:', contestHeap[0][1])
            if browser is None:
                if socket.gethostname() == 'DESKTOP-MSBHSVV':
                    PATH = "ChromeDrivers/chromedriver_windows.exe"
                    browser = webdriver.Chrome(PATH)
                else:
                    browser = webdriver.Chrome()

                # Navigating to draftkings.com
                browser.get(url="https://www.draftkings.com/")

                try:
                    # Entering email address
                    userNameField = browser.find_element_by_name("username")
                    userNameField.send_keys(creds.email)

                    # Entering password
                    passwordField = browser.find_element_by_name("password")
                    passwordField.send_keys(creds.password)

                    # Clicking login button
                    browser.find_element_by_xpath("""//*[@id="react-mobile-home"]/section/section[2]/div[3]/div[1]/button""").click()
                except execeptions.NoSuchElementException:
                    return

                time.sleep(2)

            contestTime, contestID = heapq.heappop(contestHeap)

            if get_selections(cursor, connection, contestID, browser) == -1:
                conn.close()
                return -1
            connection.commit()
        # Otherwise its not, so we'll go to sleep until it happens
        else:
            if browser is not None:
                browser.close()
                browser = None
            print('ContestID:', contestHeap[0][1])
            nextContestTime = nextContestTime.replace(tzinfo=timezone('UTC'))
            print(f"Sleeping until: {nextContestTime.astimezone('US/Pacific').strftime('%Y-%m-%d %H-%M-%S')}")
            time.sleep(difference + 60)
        # break

    if browser is not None:
        browser.close()

    conn.close()
    record_script_execution('get_selections')


if __name__ == '__main__':
    main()
