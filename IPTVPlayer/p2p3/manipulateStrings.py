# macro to load functions from correct modules depending on the python version
# build to simplify loading modules in e2iplayer scripts
# just change:
#   from urlib import
# to:
#   from Plugins.Extensions.IPTVPlayer.p2p3.manipulateStrings import 
#
from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

def strDecode(text):
    if isPY2():
        retVal = text
    else: #PY3
        retVal = text.decode(encoding='utf-8', errors='strict')
    return retVal

def iterDictItems(myDict):
    if isPY2():
        return myDict.iteritems()
    else:
        return myDict.items()