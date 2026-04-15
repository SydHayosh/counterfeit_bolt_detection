from RPLCD.i2c import CharLCD
import time
import board
import digitalio
import numpy as np

UP = digitalio.DigitalInOut(board.D6)#5
DWN = digitalio.DigitalInOut(board.D5)#6
L = digitalio.DigitalInOut(board.D13)#12
R = digitalio.DigitalInOut(board.D12)#13
MID = digitalio.DigitalInOut(board.D19)#19

inputPins = [UP, DWN, L, R, MID]
inputNames = ['UP', 'DWN', 'L', 'R', 'MID']

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

#button pins
up = 10
down = 11
select = 12

def startTest():
    print("Begin Test selected")

def exportData():
    print("Data Export selected")

def settings():
    print("Settings selected")

def debugMenu():
    print("Debug Menu selected")

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
def display_menu():# use lcd.write_string instead of lcd.write
    lcd.clear()

    if (currentIndex == topDisplayIndex):
        try:
          
          lcd.cursor_pos = (0,0)#(row, col)
          lcd.write_string(f"-> {topDisplayIndex+1}. " + mainMenu[topDisplayIndex].name)
          
          lcd.cursor_pos = (1,0)
          lcd.write_string(f"   {topDisplayIndex+2}. " + mainMenu[topDisplayIndex+1].name)
          
          print(f"-> {topDisplayIndex+1}. " + mainMenu[topDisplayIndex].name)
          print(f"   {topDisplayIndex+2}. " + mainMenu[topDisplayIndex+1].name)
          
          # Keep it displayed for a while
          time.sleep(10)
          
        except Exception as e:
          print("Error:", e)
        
    
    else:
        try:
          
          lcd.cursor_pos = (0,0)#(row, col)
          lcd.write_string(f"   {topDisplayIndex+1}. " + mainMenu[topDisplayIndex].name)
          
          lcd.cursor_pos = (1,0)
          lcd.write_string(f"-> {topDisplayIndex+2}. " + mainMenu[topDisplayIndex+1].name)
          
          print(f"   {topDisplayIndex+1}. " + mainMenu[topDisplayIndex].name)
          print(f"-> {topDisplayIndex+2}. " + mainMenu[topDisplayIndex+1].name)
          
          
        except Exception as e:
          print("Error:", e)
        


# add to menu
mainMenu.append(MenuOption("Begin Test", startTest))
mainMenu.append(MenuOption("Data Export", exportData))
mainMenu.append(MenuOption("Settings", settings))
mainMenu.append(MenuOption("Debug Menu", debugMenu))

lastState = [True] * len(inputPins)

display_menu()

while True:
    for i in range(len(inputPins)):
        currentState = inputPins[i].value
        
        if lastState[i] == True and currentState == False:
            print(f"{inputNames[i]} pressed")
            if(inputPins[i] == DWN and currentIndex+1 < len(mainMenu)):
                currentIndex += 1
                if(currentIndex > topDisplayIndex + 1):
                    topDisplayIndex += 1
        
            elif(inputPins[i] == UP and currentIndex > 0):
                print(f"The current index is {currentIndex}")
                print(f"The top of the display index is {topDisplayIndex}")
                currentIndex -= 1
                
                if(currentIndex <= topDisplayIndex - 1):
                    topDisplayIndex -= 1
                  
            display_menu()
            
        lastState[i] = currentState
        
    time.sleep(0.05)
