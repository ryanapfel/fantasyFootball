
from selenium import webdriver
import time
import selenium.webdriver.chrome.service as service
import selenium.webdriver.common.keys as keys
from selenium.webdriver.common.action_chains import ActionChains
from  selenium.webdriver.common.keys import Keys
import numpy as np
from team import Team
from roster import Slot
from player import Player






class Account:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.ESPN_USERNAME = "trojansrck123"
        self.ESPN_PASSWORD = "netLife051"
        self.teams = []

        self.driver.get("http://www.espn.com/fantasy/")


    def login(self):
        logIn = self.driver.find_element_by_class_name("user")
        button = self.driver.find_element_by_xpath("//*[@class='account-management']/li[position()=4]")
        ActionChains(self.driver).move_to_element(logIn).click().pause(1).perform()
        ActionChains(self.driver).move_to_element(button).click().pause(1).perform()
        ActionChains(self.driver).send_keys(self.ESPN_USERNAME).perform()
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        ActionChains(self.driver).send_keys(self.ESPN_PASSWORD).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER).pause(2).perform()

    def getTeams(self):
        fantasy = self.driver.find_element_by_class_name("fantasy")
        ActionChains(self.driver).move_to_element(fantasy).click().perform()
        try:
            teamsList = fantasy.find_elements_by_class_name("team")
            for index, team in enumerate(teamsList):
                url = team.find_element_by_tag_name("a").get_attribute("href")
                self.teams.append(Team(url))
        except:
            print("No Teams Have Been Found")

    def close(self):
        self.driver.close()


    def setBasketballLineup(self, index, research=True):
        team = self.teams[index]
        if research:
            team.url = team.url + "&view=research"

        self.driver.get(team.url )


        play = Player(0,self.driver)
        play2 = Player(2,self.driver)
        play.printPlayer()
        play2.printPlayer()

myA = Account()
myA.login()
myA.getTeams()
myA.setBasketballLineup(3)
myA.close()
