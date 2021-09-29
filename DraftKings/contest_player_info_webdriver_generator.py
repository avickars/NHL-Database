from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import mysql.connector.errors as Errors
import pandas as pd
from selenium import webdriver
import selenium.common.exceptions as execeptions
import time
import zipfile
import os
import csv


def get_selections(cursor, connection):
    PATH = "chromedriver.exe"
    browser = webdriver.Chrome(PATH)
    email = "aidanvickars@gmail.com"
    password = "Lgs3shrJkMFUdwf"

    contestIDs = pd.read_sql_query(f"select contestID from draft_kings.contest_details where DATE(contestStartTime) = CURRENT_DATE()", connection)

    # for index, contestID in contestIDs.iterrows():
    #     print('hello')
    contestID = 114553969

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
    browser.get(url=f"https://www.draftkings.com/draft/contest/{contestID}#/")

    time.sleep(2)

    # # Handling that stupid pop-up
    # try:
    #     browser.find_element_by_xpath("/html/body/div[11]/div/div/div/div[3]/div/button/span").click()
    # except execeptions.NoSuchElementException:
    #     print("No Popup")
    #
    # time.sleep(2)

    # Downloading the file
    browser.find_element_by_xpath("/html/body/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div/div[4]/ul[2]/li[3]/a").click()

    time.sleep(2)

    if os.environ['COMPUTERNAME'] == 'DESKTOP-MSBHSVV':
        with open("C:/Users/Aidan/Downloads/DKSalaries.csv", "r") as file:
            players = pd.read_csv(file)
            file.close()

    for index, player in players.iterrows():
        cursor.execute(f"insert into draft_kings.draft_groups_players_webdriver values (\"{player['Position']}\", "
                       f"\"{player['Name']}\", "
                       f"{player['ID']},"
                       f"\"{player['Roster Position']}\","
                       f"{player['Salary']}, "
                       f"\"{player['Game Info']}\", "
                       f"\"{player['TeamAbbrev']}\","
                       f"{player['AvgPointsPerGame']},"
                       f"{contestID})")

    os.remove("C:/Users/Aidan/Downloads/DKSalaries.csv")


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
