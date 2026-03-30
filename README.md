This branch is dedicated to the code that will be ran directly on the Rpi

========================================================================
frameworkMagnetics - Folder dedicated to the Hall Sensor stage
  -hallReader.py
    Reads inputs from Hall Sensor, compares to established dataset, returns Pass/Fail to inspectStager.py

========================================================================
frameworkOIU - Folder dedicated to Optical Inspection Unit (OIU) stage
  -inputCV
    Folder that holds preprocessed photos to be inspected by CV software
  -cameras.bash
    Controls cameras on CV, outputs them into photoRaw
  -mainOIU.py
    Handles OIU staging. Calls in order cameras.bash -> processing softwares -> openCV softwares

========================================================================
frameworkOperator - Folder dedicated to operator interactions and test staging
  -dataOut
    Folder that has test results
  -dataIO.py
    Handles outputting failed bolt photos to allow them to be placed into USB
  -displayLCD.py
    LCD display, lets user interact with device. Menu options, button interactions etc
  -inspectStager.py
    Initiates test stages in order, waits for outputs from each stage. Stores results into dataOut
    
