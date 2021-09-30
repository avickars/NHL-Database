from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
import pandas as pd
from selenium import webdriver
import selenium.common.exceptions as execeptions
import time
import zipfile
import os
import socket


def get_selections(cursor, connection, contestID):
    if socket.gethostname() == 'DESKTOP-MSBHSVV':
        PATH = "ChromeDrivers/chromedriver_windows.exe"
    browser = webdriver.Chrome(PATH)
    email = "aidanvickars@gmail.com"
    password = "Lgs3shrJkMFUdwf"

    # Navigating to draftkings.com
    browser.get(url="https://www.draftkings.com/")

    try:
        # Entering email address
        userNameField = browser.find_element_by_name("username")
        userNameField.send_keys(email)

        # Entering password
        passwordField = browser.find_element_by_name("password")
        passwordField.send_keys(password)

        # Clicking login button
        browser.find_element_by_xpath("""//*[@id="react-mobile-home"]/section/section[2]/div[3]/div[1]/button""").click()
    except execeptions.NoSuchElementException:
        return

    time.sleep(2)

    # Navigating to contest information page
    try:
        browser.get(url=f"https://www.draftkings.com/contest/gamecenter/{contestID}#/")
    except execeptions.NoSuchElementException:
        return

    time.sleep(2)

    # Handling that stupid pop-up
    try:
        browser.find_element_by_xpath("/html/body/div[11]/div/div/div/div[3]/div/button/span").click()
    except execeptions.NoSuchElementException:
        print("No Popup")

    time.sleep(2)

    # Downloading the file
    try:
        browser.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div[3]/div[1]/div[1]/div[1]/div/div[3]/div/a/span").click()
    except execeptions.NoSuchElementException:
        return

    time.sleep(2)

    # Reading the file
    if socket.gethostname() == 'DESKTOP-MSBHSVV':
        zf = zipfile.ZipFile(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")
        selections = pd.read_csv(zf.open(f"contest-standings-{contestID}.csv"))
        zf.close()
    else:
        zf = zipfile.ZipFile(f"/home/pi/Downloads/contest-standings-{contestID}.zip")
        selections = pd.read_csv(zf.open(f"contest-standings-{contestID}.csv"))
        zf.close()

    for index, selection in selections.iterrows():
        cursor.execute(f"insert into draft_kings.contest_player_selections values ({selection['EntryId']}, "
                       f"\"{selection['EntryName']}\", "
                       f"\"{selection['Lineup']}\","
                       f"{contestID})")

    if socket.gethostname() == 'DESKTOP-MSBHSVV':
        os.remove(f"C:/Users/Aidan/Downloads/contest-standings-{contestID}.zip")
    else:
        os.remove(f"contest-standings-{contestID}.csv")


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
