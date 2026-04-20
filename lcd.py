import numpy as np

def updateMenu(newMenu):
    global currentMenu, currentIndex, topDisplayIndex
    currentMenu = newMenu
    currentIndex = 0
    topDisplayIndex = 0


# Main menu options
def startTest():
    print("Begin Test selected")

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
    

class MenuOption:
    def __init__(self, name, action = None):
        self.name = name
        self.action = action
        #self.children = children or [] #incase we add submenus

# class MenuAndSubmenus:
#     def __init__(self, menuOptions, currentIndex = 0, topDisplayIndex = 0):
#         self.menuOptions = menuOptions
#         self.currentIndex = currentIndex
#         self.topDisplayIndex = topDisplayIndex


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
settingsMenu.append(MenuOption("Advanced Settings", advSettings))

advSettingsMenu.append(MenuOption("Magnetic criteria", magCriteria))
advSettingsMenu.append(MenuOption("Mag Test Duration", magTestDuration))
advSettingsMenu.append(MenuOption("Change Bolt-type", changeBolt))
advSettingsMenu.append(MenuOption("Update", update))

debugMenu.append(MenuOption("Check Connections", pinCheck))
debugMenu.append(MenuOption("Camera Test", cameraTest))
debugMenu.append(MenuOption("Magnetics Calibration", magCalibration))
debugMenu.append(MenuOption("LED Test", ledTest))



while True:
    print("-----------------------\n\n\n")
    display_menu()
    toggle = input()
    while(toggle != "w" and toggle != "s" and toggle != "d" and toggle != "a"):
        toggle = input()

    
    if(toggle == "s" and currentIndex+1 < len(currentMenu)):
        currentIndex += 1
        if(currentIndex > topDisplayIndex + 1):
            topDisplayIndex += 1

    elif(toggle == "w" and currentIndex > 0):
        print(f"The current index is {currentIndex}")
        print(f"The top of the display index is {topDisplayIndex}")
        currentIndex -= 1
        
        if(currentIndex <= topDisplayIndex - 1):
            topDisplayIndex -= 1
    elif(toggle == "d"):
        currentMenu[currentIndex].action()

    elif(toggle == "a"):
        updateMenu(mainMenu)
    
    
