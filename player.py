from selenium import webdriver
import time
import selenium.webdriver.chrome.service as service
import selenium.webdriver.common.keys as keys
from selenium.webdriver.common.action_chains import ActionChains
from  selenium.webdriver.common.keys import Keys
import numpy as np



class Player:
    def __init__(self,index,driver):
        self.driver = driver
        self.fullTable = self.driver.find_element_by_xpath("//table[@class='Table2__right-aligned Table2__table-fixed Table2__Table--fixed--left Table2__table']//tbody[@class='Table2__tbody']")
        self.index = index
        self.updateInfo()


    def updateInfo(self):
        name = "//tr[@data-idx=%d]/td[2]/div" % self.index
        team = "//tr[@data-idx=%d]/td[2]/div/div/div[2]/div/div[2]/span[1]" % self.index
        positions = "//tr[@data-idx=%d]/td[2]/div/div/div[2]/div/div[2]/span[2]" % self.index
        self.team = self.fullTable.find_element_by_xpath(team).text
        self.positions = self.fullTable.find_element_by_xpath(positions).text.strip().split(',')
        self.name =  self.fullTable.find_element_by_xpath(name).get_attribute("title")
        self.findNumPositions()
        self.isGuard()
        self.isForward()

    def isInjured(self):
        tempPath = "//tr[@data-idx=%d]//*[@title='Out']" % self.index
        try:
            self.fullTable.find_element_by_xpath(tempPath).text
        except:
            return False
        return True


    def isForward(self):
        for i in self.positions:
            if i == 'SF' or i == 'PF':
                self.isForward = True
        self.isForward = False

    def isGuard(self):
        for i in self.positions:
            if i == 'SG' or i == 'PG':
                self.isGuard = True
        self.isGuard = False

    def findNumPositions(self):
        numPos = 0
        numPos += len(self.positions)

        if self.isForward():
            numPos += 1

        if self.isGuard():
            numPos += 1

        self.numPositions = numPos

    def hasGame(self):
        game = "//tr[@data-idx=%d]/td[4]/div" % self.index
        opponent = self.fullTable.find_element_by_xpath(game).text

        if opponent == "--":
            self.opponent = "None"
            return False
        else:
            self.opponent =  opponent
            return True


    def printPlayer(self):
        print("Name :" , self.name)
        print("Position(s) :", self.positions)
        print("Team :" , self.team)
        print("Opponent", self.opponent)
