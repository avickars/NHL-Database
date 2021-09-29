from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import mysql.connector.errors as Errors
import pandas as pd
from selenium import webdriver
import selenium.common.exceptions as execeptions
import time
import zipfile
import os


def get_selections(cursor, connection):
    PATH = "chromedriver.exe"
    browser = webdriver.Chrome(PATH)
    email = "aidanvickars@gmail.com"
    password = "Lgs3shrJkMFUdwf"

    # contestIDs = pd.read_sql_query(f"select contestID from draft_kings.contest_details where DATE(contestStartTime) = CURRENT_DATE()", connection)

    # for index, contestID in contestIDs.iterrows():
    #     print('hello')
    contestID = 114464494

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

    time.sleep(2)

    # Navigating to contest information page
    browser.get(url=f"https://www.draftkings.com/contest/gamecenter/{contestID}#/")

    time.sleep(2)

    # Handling that stupid pop-up
    try:
        browser.find_element_by_xpath("/html/body/div[11]/div/div/div/div[3]/div/button/span").click()
    except execeptions.NoSuchElementException:
        print("No Popup")

    time.sleep(2)

    entries = browser.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div")

    for entry in entries.find_elements_by_tag_name('div'):
        print(entry.text)
    # for entry in entries:
    #     entry.click()

    time.sleep(2)


    # Downloading the file
    # browser.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[3]/div/a/span").click()
    #
    # time.sleep(2)
    #
    # # Reading the file
    # zf = zipfile.ZipFile(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")
    # df = pd.read_csv(zf.open(f"contest-standings-{contestID}.csv"))
    # # print(df)
    # # time.sleep(2)
    # # os.remove(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")
    #
    # if os.environ['COMPUTERNAME'] == 'DESKTOP-MSBHSVV':
    #     zf = zipfile.ZipFile(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")
    #     selections = pd.read_csv(zf.open(f"contest-standings-{contestID}.csv"))
    #     zf.close()
    #
    # # for index, selection in selections.iterrows():
    # #
    # #     cursor.execute(f"insert into draft_kings.contest_player_selections values ({selection['EntryId']}, "
    # #                    f"\"{selection['EntryName']}\", "
    # #                    f"\"{selection['Lineup']}\","
    # #                    f"{contestID})")
    #
    # os.remove(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()
    get_selections(cursor, connection)
    connection.commit()

    conn.close()


if __name__ == '__main__':
    main()
