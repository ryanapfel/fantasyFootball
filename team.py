
from selenium import webdriver
import time
import selenium.webdriver.chrome.service as service
import selenium.webdriver.common.keys as keys
from selenium.webdriver.common.action_chains import ActionChains
from  selenium.webdriver.common.keys import Keys
import numpy as np
from roster import Slot


class Team:
    def __init__(self,url):
        self.name = "Undefined Team"
        self.url = url
        self.type = "Field Hockey"
        self.record = "0-0"
        self.roster = []

    def printTeam(self):
        print("Name ", self.name)
        print("Url ", self.url)
        print("Wins ", self.wins)
        print("----------------")

    def updateTeamInfo(self, index, driver):
        self.name = driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]/span[1]").text
        self.record = driver.find_element_by_xpath("//span[@class='team-record fw-bold']").text

    def updateRoster(self):
        pass
