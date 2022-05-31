from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

def strDecode(text):
    if isPY2():
        retVal = text
    else: #PY3
        retVal = text.decode(encoding='utf-8', errors='strict')
    return retVal
