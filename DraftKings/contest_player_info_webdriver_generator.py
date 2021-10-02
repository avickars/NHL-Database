from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from selenium import webdriver
import time
import os
from datetime import datetime
import socket
import selenium.common.exceptions as execeptions
from DraftKings.DraftKingsCredentials import DraftKingsCredentialsCredentials


def get_player_info_webdriver(cursor, connection):
    if socket.gethostname() == 'DESKTOP-MSBHSVV':
        PATH = "ChromeDrivers/chromedriver_windows.exe"
        browser = webdriver.Chrome(PATH)
    else:
        browser = webdriver.Chrome()

    creds = DraftKingsCredentialsCredentials()

    email = creds.email
    password = creds.password

    contests = pd.read_sql_query(
        f"select contestID, draftGroupId from draft_kings.contest_details where contestStartTime >= CONVERT_TZ(\'{datetime.today().date()} 0:00:00\','right/US/Pacific','UTC') and contestStartTime <= CONVERT_TZ(\'{datetime.today().date()} 23:59:59\','right/US/Pacific','UTC')",
        connection)

    try:
        # Navigating to draftkings.com
        browser.get(url="https://www.draftkings.com/")

        # Entering email address
        userNameField = browser.find_element_by_name("username")
        userNameField.send_keys(email)

        # Entering password
        passwordField = browser.find_element_by_name("password")
        passwordField.send_keys(password)

        # Clicking login button
        browser.find_element_by_xpath("""//*[@id="react-mobile-home"]/section/section[2]/div[3]/div[1]/button""").click()
    except execeptions.NoSuchElementException:
        return -1

    for index, contest in contests.iterrows():
        print(contest['contestID'])

        time.sleep(2)

        # # Navigating to contest information page
        browser.get(url=f"https://www.draftkings.com/draft/contest/{contest['contestID']}/")

        time.sleep(2)

        # Handling that stupid pop-up
        try:
            browser.find_element_by_xpath("/html/body/div[11]/div/div/div/div[3]/div/button/span").click()
        except execeptions.NoSuchElementException:
            print("No Popup")

        time.sleep(2)

        try:
            # Downloading the file
            browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div/div[4]/ul[2]/li[3]/a").click()
        except execeptions.NoSuchElementException:
            print("Couldn't download file, skipped ****************************************")
            continue

        time.sleep(2)

        if socket.gethostname() == 'DESKTOP-MSBHSVV':
            with open("C:/Users/Aidan/Downloads/DKSalaries.csv", "r") as file:
                players = pd.read_csv(file)
                file.close()
        else:
            with open("/home/pi/Downloads/DKSalaries.csv", "r") as file:
                players = pd.read_csv(file)
                file.close()

        for index2, player in players.iterrows():
            try:
                cursor.execute(f"insert into draft_kings.draft_groups_players_webdriver values (\"{player['Position']}\", "
                               f"\"{player['Name']}\", "
                               f"{player['ID']},"
                               f"\"{player['Roster Position']}\","
                               f"{player['Salary']}, "
                               f"\"{player['Game Info']}\", "
                               f"\"{player['TeamAbbrev']}\","
                               f"{player['AvgPointsPerGame']},"
                               f"{contest['contestID']})")
            except execeptions.NoSuchElementException:
                # if this happens, its broken, and we are exiting
                connection.rollback()
                return -1

        if socket.gethostname() == 'DESKTOP-MSBHSVV':
            os.remove("C:/Users/Aidan/Downloads/DKSalaries.csv")
        else:
            os.remove("/home/pi/Downloads/DKSalaries.csv")

        # Now getting the scoring for events
        # Getting it here since its on the same page
        try:
            # Clicking "Full Contest Details
            browser.find_element_by_class_name('_2XCxvDE2uWbmtH2QTVQoSH').click()
        except execeptions.NoSuchElementException:
            # connection.rollback()
            print("Failed: Clicking Full Contest Details ****************************************")

        time.sleep(2)
        try:
            # Clicking "RULES & SCORING" in the popup
            browser.find_element_by_xpath('//*[@id="modal-rules-tab"]').click()

            time.sleep(2)

            # Finding players table
            # playersTable = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div/table[1]/tbody')
            playersTable = browser.find_element_by_class_name('left-table')
            playersTable = playersTable.find_element_by_tag_name('tbody')

            for row in playersTable.find_elements_by_tag_name('tr'):
                query = f"insert into draft_kings.points_legend values (\'player\',"
                for item in row.find_elements_by_tag_name('td'):
                    query += f"\'{item.text}\',"
                query += f"{contest['contestID']})"
                cursor.execute(query)
        except execeptions.NoSuchElementException:
            # connection.rollback()
            print("Failed: RULES & SCORING - Players ****************************************")
            # continue

        try:
            # goaliesTable = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div/table[2]/tbody')
            goaliesTable = browser.find_element_by_class_name('right-table')
            goaliesTable = goaliesTable.find_element_by_tag_name('tbody')

            for row in goaliesTable.find_elements_by_tag_name('tr'):
                query = f"insert into draft_kings.points_legend values (\'goalie\',"
                for item in row.find_elements_by_tag_name('td'):
                    query += f"\'{item.text}\',"
                query += f"{contest['contestID']})"
                cursor.execute(query)
        except execeptions.NoSuchElementException:
            # connection.rollback()
            print("Failed: RULES & SCORING - Goalies ****************************************")
            # continue

        # Getting the "LineUp Requirement"
        try:
            lineUpRequirement = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[2]/div[1]/div/div[2]/div/p[7]').text
            if len(lineUpRequirement) == 0:
                try:
                    lineUpRequirement = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[2]/div[1]/div/div[2]/div/p[8]').text
                except execeptions.NoSuchElementException:
                    # connection.rollback()
                    print("Failed LineUp Requirement 1 ****************************************")
                    # continue
        except execeptions.NoSuchElementException:
            try:
                lineUpRequirement = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[2]/div[1]/div/div[2]/div/p[8]').text
            except execeptions.NoSuchElementException:
                # connection.rollback()
                print("Failed LineUp Requirement 2 ****************************************")
                # continue
        cursor.execute(f"insert into draft_kings.lineup_requirements values (\"{lineUpRequirement}\",{contest['contestID']})")
        connection.commit()


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    get_player_info_webdriver(cursor, connection)
    connection.commit()

    conn.close()


if __name__ == '__main__':
    main()
