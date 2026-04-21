This branch is dedicated to the code that will be ran directly on the Rpi

========================================================================
frameworkMagnetics - Folder dedicated to the Hall Sensor stage
  -hallReader.py
    Reads inputs from Hall Sensor, [compares to established dataset], returns Pass/Fail to [userControls.py]

========================================================================
frameworkOIU - Folder dedicated to Optical Inspection Unit (OIU) stage
  -inputCV
    Folder that holds preprocessed photos to be inspected by CV software
  -[cameras.sh]
    Controls cameras on CV, outputs them into photoRaw
  -[mainOIU.py]
    Handles OIU staging. Calls in order cameras.bash -> processing softwares -> openCV softwares, sends outputs to dataOut. Create subfolder in dataOut, then deposit the output      in the subfolder
  -standardized_markings.py
    Inspects bolthead markings
  -[dimensions.py]
    Verifies pitch diameter on bolts. [MUST ESTABLISH PIXEL:INCH RATIO.]
  
========================================================================
frameworkOperator - Folder dedicated to operator interactions and test staging
  -dataOut
    Folder that has test results
  -[dataIO.py]
    Handles copying folders in dataOut into USB.
  -[userControls.py]
    LCD display, lets user interact with device. Menu options, button interactions etc. [Initiates test stages in order, waits for outputs from each stage. Stores results into        dataOut]. Calls lightsOn.py when needed
  -lightsOn.py
    Controls LEDs in response to user input. 
  
    
