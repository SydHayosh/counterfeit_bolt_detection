import numpy as np
import RPi.GPIO as GPIO

#button pins
up = 10
down = 11
select = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(up, GPIO.IN)
    GPIO.setup(down, GPIO.IN)
    GPIO.setup(select, GPIO.IN)

class MenuOption:
    def __init__(self, name, action = None):
        self.name = name
        self.action = action
        #self.children = children or [] #incase we add submenus

# variables
mainMenu = []
currentIndex = 0
topDisplayIndex = 0 #When the menu is greater then 2 options 


# functions
def display_menu():
    lcd.clear
    lcd.write(0,0, mainMenu[topDisplayIndex].name)
    lcd.write(0,0, mainMenu[topDisplayIndex+1].name)


# add to menu
mainMenu.append(MenuOption("Run Test"))

while True:
    display_menu()
    