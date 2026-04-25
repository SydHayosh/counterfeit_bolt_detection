from .cameras import capture_photos
from .dimensions import countThreads
from .standardized_markings import standMarkCheck

def runTests():
    capture_photos()
    return countThreads() or standMarkCheck()