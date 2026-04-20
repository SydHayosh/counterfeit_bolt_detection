from frameworkMagnetics.hallReader import setup_read_dataset, mag_test
from RPLCD.i2c import CharLCD
import time
import board
import digitalio
import numpy as np

# Sets direction to pins
UP = digitalio.DigitalInOut(board.D6)#5
DWN = digitalio.DigitalInOut(board.D5)#6
L = digitalio.DigitalInOut(board.D13)#12
R = digitalio.DigitalInOut(board.D12)#13
MID = digitalio.DigitalInOut(board.D19)#19

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

# Sets the pins default state and type
for pin in inputPins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
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

# Main menu options
def startTest():
    print("Begin Test selected")
    mag_test(10.15) #test value hallReader.py should get this value on its own

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
    print("Advanced Settings selected")
    updateMenu(advSettingsMenu)


# Advanced settings menu options
def magCriteria():
    print("Magnetic criteriat selected")

def magTestDuration():
    print("Mag Test Duration selected")

def changeBolt():
    print("Change Bolt-type selected")

def update():
    print("Update selected")


# Debug menu options
def pinCheck():
    print("Check Connections selected")

def cameraTest():
    print("Camera Test selected")

def magCalibration():
    print("Magnetics Calibration selected")

def ledTest():
    print("LED Test selected")

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
settingsMenu.append(MenuOption("Advanced Settings", advSettings))

advSettingsMenu.append(MenuOption("Magnetic criteria", magCriteria))
advSettingsMenu.append(MenuOption("Mag Test Duration", magTestDuration))
advSettingsMenu.append(MenuOption("Change Bolt-type", changeBolt))
advSettingsMenu.append(MenuOption("Update", update))

debugMenu.append(MenuOption("Check Connections", pinCheck))
debugMenu.append(MenuOption("Camera Test", cameraTest))
debugMenu.append(MenuOption("Magnetics Calibration", magCalibration))
debugMenu.append(MenuOption("LED Test", ledTest))


lastState = [True] * len(inputPins)

# Reads the ideal bolt magnetic dataset
setup_read_dataset()

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
