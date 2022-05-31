from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

if isPY2():
    import Plugins.Extensions.IPTVPlayer.p2p3.thread
else:
    import _thread as thread
