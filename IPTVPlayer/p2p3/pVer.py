import sys

pyVersion = sys.version_info[0]

def isPY2():
    if pyVersion == 2:
        return True
    else:
        return False
