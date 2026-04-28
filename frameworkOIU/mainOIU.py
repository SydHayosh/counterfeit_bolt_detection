from .cameras import capture_photos
from .dimensions import countThreads
from ledTest import ledCheck, setRegion, RED, GREEN, BLUE, WHITE, OFF, TOP, HEAD, SHAFT
from .standardized_markings import standMarkCheck
from .color import colorCheck



def runTests():
    setRegion(HEAD, WHITE)
    colorCheck()
    setRegion(HEAD, BLUE)
    setRegion(SHAFT, WHITE)
    capture_photos()
    countThreads()
    standMarkCheck()
    setRegion(HEAD, OFF)
    setRegion(SHAFT, OFF)


runTests()