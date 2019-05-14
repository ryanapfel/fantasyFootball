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
        self.fullTable = self.driver.find_element_by_xpath("//tbody[@class='Table2__tbody']")
        self.index = index
        self.updateInfo()


    def updateInfo(self):
        name = "//tr[@data-idx=%d]/td[2]/div" % self.index
        team = "//tr[@data-idx=%d]/td[2]/div/div/div[2]/div/div[2]/span[1]" % self.index
        positions = "//tr[@data-idx=%d]/td[2]/div/div/div[2]/div/div[2]/span[2]" % self.index
        pr = "//tr[@data-idx=%d]/td[10]/div" % self.index

        self.positionRank = self.fullTable.find_element_by_xpath(pr).text
        self.team = self.fullTable.find_element_by_xpath(team).text
        self.positions = self.fullTable.find_element_by_xpath(positions).text.strip().split(',')
        self.name =  self.fullTable.find_element_by_xpath(name).get_attribute("title")
        self.findNumPositions()
        self.isGuard()
        self.isForward()

    def isHealthy(self):
        tempPath = "//tr[@data-idx=%d]//*[@title='Out']" % self.index
        try:
            self.fullTable.find_element_by_xpath(tempPath).text
        except:
            return True
        return False


    def onBench(self):
        if self.index > 9:
            return True
        else:
            return False


    def isForward(self):
        for i in self.positions:
            if i == 'SF' or i == 'PF':
                self.forward = True
        self.forward = False

    def isGuard(self):
        for i in self.positions:
            if i == 'SG' or i == 'PG':
                self.guard = True
        self.guard = False

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

    def movePlayerTo(self, destinationIndex):
        '''
        param: gives the index of the location where we want to move this player to
                assumes location is valid for that player
        response: moves player to that location
        '''
        sleep = 0

        buttonPath = "//tr[@data-idx=%d]/td[3]/div/div/a" % self.index
        button = self.driver.find_element_by_xpath(buttonPath)

        coordinates = button.location_once_scrolled_into_view # returns dict of X, Y coordinates
        coordinates['x'] -= 100 # adjusts location so it gives room at the top to click correctly
        coordinates['y'] -= 100
        self.driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

        ActionChains(self.driver).click(button).pause(sleep).perform()


        destinationButtonPath = "//tr[@data-idx=%d]/td[3]/div/div/a" % destinationIndex
        destButton = self.driver.find_element_by_xpath(destinationButtonPath)

        coordinates = destButton.location_once_scrolled_into_view # returns dict of X, Y coordinates
        coordinates['x'] -= 100 # adjusts location so it gives room at the top to click correctly
        coordinates['y'] -= 100
        self.driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))

        ActionChains(self.driver).click(destButton).pause(sleep).perform()
        self.index = destinationIndex





    def printPlayer(self):
        print(self.name, " ---> Position(s) :", self.positions, "--> Team :" , self.team)
