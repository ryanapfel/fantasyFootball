from selenium import webdriver
import time
import selenium.webdriver.chrome.service as service
import selenium.webdriver.common.keys as keys
from selenium.webdriver.common.action_chains import ActionChains
from  selenium.webdriver.common.keys import Keys
import numpy as np
from player import Player

class Slot:
    def __init__(self,index,driver):
        self.driver = driver
        self.fullTable = self.driver.find_element_by_xpath("//table[@class='Table2__right-aligned Table2__table-fixed Table2__Table--fixed--left Table2__table']//tbody[@class='Table2__tbody']")
        self.index = index
        self.updatePosition()
        self.currentPlayer()

    def updatePosition(self):
        tempPath = "//tr[@data-idx=%d]/td[1]/div" % self.index
        self.position =  self.fullTable.find_element_by_xpath(tempPath).get_attribute("title")

    def currentPlayer(self):
        tempPath = "//tr[@data-idx=%d]/td[2]/div" % self.index
        self.player =  self.fullTable.find_element_by_xpath(tempPath).get_attribute("title")

    def hasPlayer(self):
        return not (self.player == "Player")

    def clickSlot(self, sleep=0):
        tempPath = "//tr[@data-idx=%d]/td[3]/div/div/a" % self.index
        button = self.fullTable.find_element_by_xpath(tempPath)
        ActionChains(self.driver).move_to_element(button).click().pause(sleep).perform()

    def printSlot(self):
        print(self.position, self.player, self.index)
