from frameworkMagnetics.magReader import magRead, cleanup
from frameworkMagnetics.magCheck import getIdealData, magTest
from ledTest import ledCheck, setRegion, RED, GREEN, BLUE, WHITE, OFF, TOP, HEAD, SHAFT
from frameworkOIU.mainOIU import runOIUTests
import frameworkMagnetics.magCheck
import atexit
from RPLCD.i2c import CharLCD
import time
import board
import digitalio
import numpy as np
from .pins import UP, DWN, L, R, MID, inputPins, inputNames

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=3,
    cols=16,
    rows=2,
    #charmap='A02'
    auto_linebreaks = False
)

def updateMenu(newMenu):
    global currentMenu, currentIndex, topDisplayIndex
    currentMenu = newMenu
    currentIndex = 0
    topDisplayIndex = 0

def startUp():
    # Reads the ideal bolt magnetic dataset
    global idealData
    #idealData = getIdealData(magCheck.acceptedNumOfStdDev)
    idealData = getIdealData(3)
    global ambient
    ambient = magRead(3)
    print(idealData)
    print(ambient)

# Main menu options =============================================================================
def startTest():
    print("Begin Test selected")
    setRegion(HEAD, WHITE)
    setRegion(SHAFT, WHITE)
    lcd.clear()
    lcd.cursor_pos = (0,0)#(row, col)
    lcd.write_string("Testing...")
    magResult = magTest(idealData, ambient)

    lcd.clear()
    lcd.cursor_pos = (0,0)#(row, col)

    if magResult:
        lcd.write_string("Magnetics Passed")
        setRegion(TOP, BLUE)
    else:
        lcd.write_string("Magnetics Failed")
        setRegion(TOP, RED)
    
    print(magResult)
    time.sleep(3)

    if magResult:
        if runOIUTests(): #test value hallReader.py should get this value on its own
            setRegion(TOP, GREEN)
            lcd.clear()
            lcd.cursor_pos = (0,0)#(row, col)
            lcd.write_string("Optical Inspect")
            lcd.cursor_pos = (1,0)#(row, col)
            lcd.write_string("Passed")
        else:
            setRegion(TOP, RED)
            lcd.clear()
            lcd.cursor_pos = (0,0)#(row, col)
            lcd.write_string("Optical Inspect")
            lcd.cursor_pos = (1,0)#(row, col)
            lcd.write_string("Failed")

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

# Settings menu options ==========================================================================
def idealBolt():
    print("Ideal Bolt selected")

def advSettings():
    print("Adv Settings selected")
    updateMenu(advSettingsMenu)

# Advanced settings menu options =================================================================
def magCriteria():
    print("Mag criteria selected")
    updateMenu(MagCriteriaMenu)

def magTestDuration():
    print("Mag Test Duration selected")

def changeBolt():
    print("Bolt-type selected")

def update():
    print("Update selected")

# Debug menu options =============================================================================
def pinCheck():
    print("Check Connections selected")

def cameraTest():
    print("Camera Test selected")

def magCalibration():
    print("Mag Calibration selected")

def ledTest():
    print("LED Test selected")
    lcd.clear()
    lcd.cursor_pos = (0,0)#(row, col)
    lcd.write_string("Cycling LEDs...")
    ledCheck()

def stdDevAllow(num):
    magCheck.acceptedNumOfStdDev = num

# class containing the menu option name and action that it preforms ===============================
class MenuOption:
    def __init__(self, name, action = None):
        self.name = name
        self.action = action

# variables

mainMenu = []
settingsMenu = []
advSettingsMenu = []
MagCriteriaMenu = []
debugMenu = []
currentIndex = 0
topDisplayIndex = 0 #When the menu is greater then 2 options 

atexit.register(cleanup)
currentMenu = mainMenu

# functions
def display_menu():# use lcd.write_string instead of lcd.write
    lcd.clear()

    if (currentIndex == topDisplayIndex):
        try:
          
          lcd.cursor_pos = (0,0)#(row, col)
          lcd.write_string(f"->{topDisplayIndex+1}." + currentMenu[topDisplayIndex].name)
          
          lcd.cursor_pos = (1,0)
          lcd.write_string(f"  {topDisplayIndex+2}." + currentMenu[topDisplayIndex+1].name)
          
          print(f"-> {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
          print(f"   {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)

          
        except Exception as e:
          print("Error:", e)
        
    
    else:
        try:
          
          lcd.cursor_pos = (0,0)#(row, col)
          lcd.write_string(f"  {topDisplayIndex+1}." + currentMenu[topDisplayIndex].name)
          
          lcd.cursor_pos = (1,0)
          lcd.write_string(f"->{topDisplayIndex+2}." + currentMenu[topDisplayIndex+1].name)
          
          print(f"   {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
          print(f"-> {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)
          
          
        except Exception as e:
          print("Error:", e)
        
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

MagCriteriaMenu.append(MenuOption("Default", lambda: stdDevAllow(2.0)))
MagCriteriaMenu.append(MenuOption("Fair", lambda: stdDevAllow(3.0)))
MagCriteriaMenu.append(MenuOption("Strict", lambda: stdDevAllow(1.0)))

debugMenu.append(MenuOption("Check Connections", pinCheck))
debugMenu.append(MenuOption("Camera Test", cameraTest))
debugMenu.append(MenuOption("Mag Calibration", magCalibration))
debugMenu.append(MenuOption("LED Test", ledTest))

lastState = [True] * len(inputPins)

startUp()

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
