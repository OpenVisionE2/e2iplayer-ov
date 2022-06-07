# macro to load functions from correct modules depending on the python version
# some functions copied from six library to support old nbox python - al credits go to it authors.
# build to simplify loading modules in e2iplayer scripts
# just change:
#   from urlib import
# to:
#   from Plugins.Extensions.IPTVPlayer.p2p3.manipulateStrings import 
#
from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

def strDecode(text,  setErrors = 'strict'):
    if isPY2():
        retVal = text
    else: #PY3
        retVal = text.decode(encoding='utf-8', errors=setErrors)
    return retVal

def iterDictItems(myDict):
    if isPY2():
        return myDict.iteritems()
    else:
        return myDict.items()

def strEncode(text,  encoding = 'utf-8'):
    if isPY2():
        retVal = text
    else: #PY3
        retVal = text.encode(encoding)
    return retVal

def ensure_binary(s, encoding='utf-8', errors='strict'): #copied from six library
    """Coerce **s** to six.binary_type.
    For Python 2:
      - `unicode` -> encoded to `str`
      - `str` -> `str`
    For Python 3:
      - `str` -> encoded to `bytes`
      - `bytes` -> `bytes`
    """
    if isinstance(s, binary_type):
        return s
    if isinstance(s, text_type):
        return s.encode(encoding, errors)
    raise TypeError("not expecting type '%s'" % type(s))
