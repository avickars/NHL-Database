from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import pandas as pd

def testing():
    print("In Test")
    print("Leaving Test")


def scrape_indv_contest_info(browser):
    contestDetails = {}
    # prizePayouts = []

    # Recording the current window handle
    tabHandle = browser.current_window_handle

    # Clicking "Full Contest Details"
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/span[1]/button/span').click()

    # Switching to popup
    browser.switch_to.window(browser.window_handles[-1])

    # Sleeping to give time to load
    time.sleep(2)

    # Getting contest details
    contestDetails['name'] = browser.find_element_by_xpath('//*[@id="dialog1Title"]').text
    contestDetails['entryFee'] = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/p').text
    contestDetails['prizes'] = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/p').text
    contestDetails['crowns'] = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/p').text
    contestDetails['multiEntries'] = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[1]/div[1]/div[2]/div[3]/div[2]/p').text
    contestDetails['summary'] = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/div').text

    # Getting prize payouts
    # entryFee = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/p').text

    prizePayoutTable = browser.find_element_by_xpath('/html/body/div[6]/div/div[9]/div/div/div[3]/div[1]/div[1]/div[2]/div/table/tbody')
    for prizePayout in prizePayoutTable.find_elements_by_tag_name('tr'):
        prizePayoutDetails = prizePayout.find_elements_by_tag_name('th')
        for prizePayoutDetail in prizePayoutDetails:
            print(prizePayoutDetail.text)
    # print(len(prizePayouts))

    print(contestDetails)


    # contestName = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/h3').text
    #
    # contestFee = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/ul/li[2]/span/span/span/span').text
    #
    # prizes = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/ul/li[3]/span/span/span/span').text
    #
    #
    # browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/div[1]/ul/li[4]/span/span/span').text
    #
    # print(contestName)
    # print(contestFee)
    # print(prizes)


def navigate_to_contest_table():
    PATH = "chromedriver.exe"
    browser = webdriver.Chrome(PATH)

    email = "aidanvickars@gmail.com"
    password = "Lgs3shrJkMFUdwf"

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

    # Clicking NHL button
    browser.find_element_by_xpath("""//*[@id="dkjs-subnav"]/div/div/ul/li[6]/span/a""").click()

    time.sleep(2)

    # Clicking "VIEW LIVE CONTESTS"
    # browser.find_element_by_xpath("""//*[@id="dkjs-game-set-live-button"]/div/div[1]/span""").click()

    time.sleep(2)

    # Getting the div tag that contains the live contests
    liveContestContainer = browser.find_element_by_xpath("""//*[@id="lobby-grid"]/div[4]/div""")

    # Getting all sub elements
    liveContestContainerSubTags = liveContestContainer.find_elements_by_xpath(".//*")

    mainWindow = browser.window_handles[0]

    # Finding the live tags
    liveContests = []
    for i in liveContestContainerSubTags:
        if i.get_attribute("role") == 'row':
            liveContests.append(i)

    # Iterating through each row in the contest table
    for liveContest in liveContests:
        # Getting the elements in each row
        elements = liveContest.find_elements_by_xpath(".//*")

        # Iterating through each element in the row
        for element in elements:
            # When we get the button we open it in a new tab
            if element.get_attribute("class") == "dk-btn dk-btn-dark":
                # Getting the link to contest info (i.e. the link under "ENTER")
                contestInfo = element.get_attribute("href")

                # Opening new tab
                browser.execute_script("window.open('');")

                # Switching to tab
                browser.switch_to.window(browser.window_handles[-1])

                # Navigating to link
                browser.get(contestInfo)

                scrape_indv_contest_info(browser)
                # contest = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div/h3')
                # print(contest.text)

                time.sleep(2)
                browser.close()
                browser.switch_to.window(mainWindow)

                break

        break

    time.sleep(2)

    browser.close()


def main():
    navigate_to_contest_table()


if __name__ == '__main__':
    main()
