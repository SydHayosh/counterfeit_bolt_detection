from .cameras import capture_photos, capture_head
from .dimensions import countThreads
from ledTest import ledCheck, setRegion, RED, GREEN, BLUE, WHITE, OFF, TOP, HEAD, SHAFT
from .standardized_markings import standMarkCheck
from .color import colorCheck



def runTests():
    setRegion(HEAD, WHITE)
    capture_head()
    color = colorCheck()
    setRegion(HEAD, BLUE)
    setRegion(SHAFT, WHITE)
    capture_photos()
    countThreads()
    standMarkCheck()
    print("Bolt color is " + color)
    setRegion(HEAD, OFF)
    setRegion(SHAFT, OFF)


runTests()