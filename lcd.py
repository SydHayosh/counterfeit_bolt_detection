import numpy as np
#import RPi.GPIO as GPIO

#button pins
up = 10
down = 11
select = 12

# def setup():
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(up, GPIO.IN)
#     GPIO.setup(down, GPIO.IN)
#     GPIO.setup(select, GPIO.IN)

def startTest():
    print("Begin Test selected")

def exportData():
    print("Data Export selected")

def settings():
    print("Settings selected")
    currentMenu = settingsMenu
    currentIndex = 0
    topDisplayIndex = 0

def debugMenu():
    print("Debug Menu selected")

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
currentIndex = 0
topDisplayIndex = 0 #When the menu is greater then 2 options

currentMenu = mainMenu


# functions
def display_menu():# use lcd.write_string instead of lcd.write
    # lcd.clear
    # lcd.write(0,0, mainMenu[topDisplayIndex].name)
    # lcd.write(0,0, mainMenu[topDisplayIndex+1].name)
    # arrowTail = "   |\n"
    # arrowHead = "   v\n"

    # if(topDisplayIndex+1 == len(mainMenu)-1):
    #     arrowTail = "\n"
    #     arrowHead = "\n"

    if (currentIndex == topDisplayIndex):
        print(f"-> {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
        print(f"   {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)
    
    else:
        print(f"   {topDisplayIndex+1}. " + currentMenu[topDisplayIndex].name)
        print(f"-> {topDisplayIndex+2}. " + currentMenu[topDisplayIndex+1].name)


# add to menu
mainMenu.append(MenuOption("Begin Test", startTest))
mainMenu.append(MenuOption("Data Export", exportData))
mainMenu.append(MenuOption("Settings", settings))
mainMenu.append(MenuOption("Debug Menu", debugMenu))

while True:
    print("-----------------------\n\n\n")
    display_menu()
    toggle = input()
    while(toggle != "w" and toggle != "s" and toggle != "d"):
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
            
    
    