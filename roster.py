from selenium import webdriver
import time
import selenium.webdriver.chrome.service as service
import selenium.webdriver.common.keys as keys
from selenium.webdriver.common.action_chains import ActionChains
from  selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from player import Player

class Slot:
    def __init__(self,index,driver):
        self.driver = driver
        self.index = index
        self.updatePosition()
        self.currentPlayer()

    def updatePosition(self):
        tempPath = "//tbody[@class='Table2__tbody']/tr[@data-idx=%d]/td[1]/div" % self.index
        self.position =  self.driver.find_element_by_xpath(tempPath).get_attribute("title")

    def currentPlayer(self):
        tempPath = "//tbody[@class='Table2__tbody']/tr[@data-idx=%d]/td[2]/div" % self.index
        self.player =  self.driver.find_element_by_xpath(tempPath).get_attribute("title")


    def hasPlayer(self):
        return not (self.player == "Player")


    def clickSlot(self, sleep=0):
        tempPath = "//tbody[@class='Table2__tbody']/tr[@data-idx=%d]/td[3]/div/div/a" % self.index
        button = self.driver.find_element_by_xpath(tempPath)
        ActionChains(self.driver).click(button).pause(sleep).perform()


    def getButton(self):
        tempPath = "//tbody[@class='Table2__tbody']/tr[@data-idx=%d]/td[1]/div" % self.index
        return self.driver.find_element_by_xpath(tempPath)

    def willFit(self, player):
        if self.index == 7 or self.index == 8 or self.index == 9:
            return True
        elif self.position == "G" and player.isGuard():
            return True
        elif self.position == "F" and player.isForward():
            return True
        elif self.position == player.position:
            return True
        else:
            return False

    def printSlot(self):
        print(self.position, self.player, self.index)


class Roster:
    def __init__(self, driver):
        self.driver = driver

        print("ROSTER RETRIEVAL START:")
        self.updatenumslots()
        self.getFullRoster()
        self.day = "12/27/2018"
        self.isSet = False
        self.cutOffTime = "11:59am"
        self.indexOfSlot = {"PG": 0,"Point Guard":0,"SG":1,"Shooting Guard":1,
                            "SF":2,"Small Forward":2,"PF":3,"Power Forward":3,
                            "C":4,"Center":4,"G":5,"Guard":5,"F":6,"Forward":6,
                            "UTIL_1":7,"UTIL_2":8,"UTIL_3":9}

    def updatenumslots(self):
        slotsNotFound = True
        timeDelay = 1
        while slotsNotFound:
            time.sleep(timeDelay)
            try:
                path = "//tbody[@class='Table2__tbody']//tr"
                slotList = self.driver.find_elements_by_xpath(path)
            except NoSuchElementException:
                print("Not Found")
            self.numslots =  len(slotList) - 1

            if self.numslots > 0 or timeDelay > 10:
                slotsNotFound = False
            timeDelay += 1

        print("Total Slots :",self.numslots)

    def getFullRoster(self):
        self.fullRoster = {}
        try:
            for i in range(self.numslots):
                if self.hasPlayer(i):
                    tempPlayer = Player(i,self.driver)
                    self.fullRoster[tempPlayer.name] = tempPlayer

            self.printPlayerDict("Full Roster", self.Full)
        except:
            print("\n Roster Retrieval Error")

    def hasPlayer(self, index, firstTry = True):
        if firstTry:
            tempPath = "//tbody[@class='Table2__tbody']/tr[@data-idx=%d]/td[2]/div" % index
            playerName =  self.driver.find_element_by_xpath(tempPath).get_attribute("title")
            if playerName == "Player":
                return False
            else:
                return True
        else:
            # less resource usage
            for key, i in self.fullRoster.items():
                if i.index == index:
                    return True
                else:
                    return False

    def printPlayerDict(self,dictTitle,dict):
        print("=========",dictTitle,"=========")
        for key,i in dict.items:
            print(key,". ", i)
        print()

    def getActivePlayers(self):
        self.activePlayers = {}
        for key,i in self.fullRoster.items():
            if i.isHealthy() and i.hasGame():
                self.activePlayers[i.name] = i

        self.printPlayerDict("Active Players", self.activePlayers)


    def move(self, playerName, targetPosition,sleep=True):
        targetIndex = self.indexOfSlot[targetPosition]
        currentPlayer = self.fullRoster[playerName]
        currentPlayerIndex = currentPlayer.index
        onBench = currentPlayer.onBench()

        if self.hasPlayer(targetIndex, firstTry = False):
            playerInTarget = True
        else:
            playerInTarget = False

        currentPlayer.movePlayerTo(targetIndex)

        if playerInTarget:
            targetPlayerName = Player(targetIndex, self.driver).name
            self.fullRoster[targetPlayerName].index = currentPlayerIndex
        elif onBench:
            # if theres no player in the target and he's coming from the bench
            for key, i in self.fullRoster.items():
                if i.index > currentPlayerIndex:
                    #if the player has a larger index then he is below and we need to subtract one
                    i.index -= 1
            self.numslots -= 1

        print("======= Move ========")
        print(currentPlayer.name,"(",currentPlayer.index,")", "-->", targetPosition)
        if playerInTarget:
            print(targetPlayerName, " -->", currentPlayerIndex)
        print("=====================")

        if sleep:
            time.sleep(2)



    def moveToBench(self, playerName):
        player = getPlayer(playerName)
        currentSlot = player.index
        self.numslots += 1

        self.slots[currentSlot].clickSlot()
        newSlot = Slot(self.numslots, self.driver)
        self.slots.append(newSlot)
        self.slots[self.numslots].clickSlot()

        player.index = self.numslots








    def getLowestPosition(self, positionName):
        '''
        arg: valid position name ex: "C" , "Center"
        returns: player with highest rank and lowest number of positions
        '''
        ar = []
        if len(self.activeQueue) > 0:
            for i in self.activeQueue:
                if positionName in i.positions:
                    ar.append(i)
            sorted(ar, key=lambda player: player.numPositions) # sorts by lowest number of positions
            if len(ar) > 0:
                curNumPos = ar[0].numPositions

                for index,i in enumerate(ar):
                    if i.numPositions > curNumPos:
                        ar.pop(index)
                # sort by lowest position rank
                sorted(ar, key=lambda player: player.positionRank)

                return ar[0]
        return 0



    def popPlayer(self, playerName, given_list):
        for index,player in enumerate(given_list):
            if player.name == playerName:
                given_list.pop(index)


    def place(self):
        # find the active players
        self.getActivePlayers()
        placeIteration = 0

        while len(self.activeQueue) > 0:

            if placeIteration == 0:
                ## Place First Tier
                print("Placing First Tier: ")
                placeInOrder = ["C","PF","PG","SG","SF"]
                for tempPosition in placeInOrder:
                    tempPlayer = self.getLowestPosition(tempPosition)

                    if tempPlayer is not 0:
                        if self.isNotInSlot(tempPlayer.name,tempPosition):
                            self.move(tempPlayer.name, tempPosition)
                        self.popPlayer(tempPlayer.name, self.activeQueue)
            elif placeIteration == 1:
                print("Placing Second Tier (G,F):")
                ## Second Tier
                # guard
                placeInOrder = ["G","F"]
                for tempPosition in placeInOrder:
                    temp = []
                    for player in self.activeQueue:
                        if tempPosition == "G" and player.isGuard():
                            temp.append(player)
                        elif tempPosition == "F" and player.isForward():
                            temp.append(player)
                    if len(temp) > 0:
                        sorted(temp, key=lambda player: player.numPositions) # sorts by lowest number of positions

                        curNumPos = temp[0].numPositions

                        for index, i in enumerate(temp):
                            if i.numPositions > curNumPos:
                                temp.pop(index)
                        # sort by lowest position rank
                        sorted(temp, key=lambda player: player.positionRank)

                        placeMe = temp[0]
                        if self.isNotInSlot(placeMe.name, tempPosition):
                            self.move(placeMe.name,tempPosition)
                        self.popPlayer(placeMe.name, self.activeQueue)

            elif placeIteration == 2:
                # Final Tier -- Utility
                print("Placing Utility Tier:")
                placeInOrder = ["UTIL_1","UTIL_2","UTIL_3"]
                sorted(self.activeQueue, key=lambda player: player.positionRank)

                numLeft = len(self.activeQueue)
                numPlaced = 0

                while numLeft != 0  or numPlaced == len(placeInOrder):
                    placeMe = self.activeQueue[numPlaced]

                    if self.isNotInSlot(placeMe.name, placeInOrder[numPlaced]):
                        self.move(placeMe.name, placeInOrder[numPlaced])
                    self.popPlayer(placeMe.name, self.activeQueue)

                    numLeft -= 1
                    numPlaced += 1
            elif placeIteration == 3:
                # get all the active players in positions 0 - 6 (PG-F)
                for remainderPlayer in self.activeQueue:
                    for index in range(0,6):
                        currentSlot = self.slots[index]
                        currentPlayer = self.getPlayer(currentSlot.player)

                        if remainderPlayer.positionRank > currentPlayer.positionRank and currentSlot.willFit(remainderPlayer):
                            # player has to be on the bench if we are here
                            self.move(remainderPlayer.name, currentSlot)
                            self.popPlayer(remainderPlayer.name, currentSlot)



            placeIteration += 1
