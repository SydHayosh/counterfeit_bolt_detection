from frameworkMagnetics.magCheck import setup_read_dataset, magTest
from ledTest import ledCheck, setRegion, RED, GREEN, BLUE, WHITE, OFF, TOP, HEAD, SHAFT
from frameworkOIU.mainOIU import runTests
import time
import board
import digitalio
import numpy as np
from .pins import UP, DWN, L, R, MID, inputPins, inputNames

def updateMenu(newMenu):
    global currentMenu, currentIndex, topDisplayIndex
    currentMenu = newMenu
    currentIndex = 0
    topDisplayIndex = 0

# Main menu options
def startTest():
    print("Begin Test selected")
    setRegion(HEAD, WHITE)
    setRegion(SHAFT, WHITE)
    mag_test(10.15)
    if runTests(): #test value hallReader.py should get this value on its own
        setRegion(TOP, GREEN)
    else:
        setRegion(TOP, RED)

    setRegion(HEAD, OFF)
    setRegion(SHAFT, OFF)
    time.sleep(3)
    setRegion(TOP, OFF)
    

def exportData():
    print("Data Export selected")

def settings():
    print("Settings selected")
    updateMenu(settingsMenu)

def debugSubmenu():
    print("Debug Menu selected")
    updateMenu(debugMenu)


# Settings menu options
def idealBolt():
    print("Ideal Bolt selected")

def advSettings():
    print("Adv Settings selected")
    updateMenu(advSettingsMenu)


# Advanced settings menu options
def magCriteria():
    print("Mag criteria selected")

def magTestDuration():
    print("Mag Test Duration selected")

def changeBolt():
    print("Bolt-type selected")

def update():
    print("Update selected")


# Debug menu options
def pinCheck():
    print("Check Connections selected")

def cameraTest():
    print("Camera Test selected")

def magCalibration():
    print("Mag Calibration selected")

def ledTest():
    print("LED Test selected")
    ledCheck()

# class containing the menu option name and action that it preforms
class MenuOption:
    def __init__(self, name, action = None):
        self.name = name
        self.action = action

# variables
mainMenu = []
settingsMenu = []
advSettingsMenu = []
debugMenu = []
currentIndex = 0
topDisplayIndex = 0 #When the menu is greater then 2 options 

currentMenu = mainMenu

# functions
def display_menu():# use lcd.write_string instead of lcd.write

    if (currentIndex == topDisplayIndex):
        print(f"-> {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
        print(f"   {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)
    
    else:  
        print(f"   {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
        print(f"-> {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)
          

# Populates menu and submenus
mainMenu.append(MenuOption("Begin Test", startTest))
mainMenu.append(MenuOption("Data Export", exportData))
mainMenu.append(MenuOption("Settings", settings))
mainMenu.append(MenuOption("Debug Menu", debugSubmenu))

settingsMenu.append(MenuOption("Ideal Bolt", idealBolt))
settingsMenu.append(MenuOption("Adv Settings", advSettings))

advSettingsMenu.append(MenuOption("Mag criteria", magCriteria))
advSettingsMenu.append(MenuOption("Mag Test Duration", magTestDuration))
advSettingsMenu.append(MenuOption("Bolt-type", changeBolt))
advSettingsMenu.append(MenuOption("Update", update))

debugMenu.append(MenuOption("Check Connections", pinCheck))
debugMenu.append(MenuOption("Camera Test", cameraTest))
debugMenu.append(MenuOption("Mag Calibration", magCalibration))
debugMenu.append(MenuOption("LED Test", ledTest))


lastState = [True] * len(inputPins)

# Reads the ideal bolt magnetic dataset
setup_read_dataset()

setRegion(HEAD, BLUE)
display_menu()

while True:
    for i in range(len(inputPins)):
        currentState = inputPins[i].value
        
        if lastState[i] == True and currentState == False:
            print(f"{inputNames[i]} pressed")

            # Moves down the current menu options
            if(inputPins[i] == DWN and currentIndex+1 < len(currentMenu)):
                currentIndex += 1
                if(currentIndex > topDisplayIndex + 1):
                    topDisplayIndex += 1
                display_menu()

            # Moves up the current menu options
            elif(inputPins[i] == UP and currentIndex > 0):
                currentIndex -= 1
                
                if(currentIndex <= topDisplayIndex - 1):
                    topDisplayIndex -= 1
                display_menu()

            # Selects current highlighted menu options
            elif(inputPins[i] == MID or inputPins[i] == R):
                currentMenu[currentIndex].action()
                display_menu() #TODO maybe move this to updateMenu
            
            # Goes back to main menu
            elif(inputPins[i] == L):
                updateMenu(mainMenu)
                display_menu() #TODO maybe move this to updateMenu
            
            
        lastState[i] = currentState
        
    time.sleep(0.05)
