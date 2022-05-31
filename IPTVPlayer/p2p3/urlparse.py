from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

if isPY2():
    import urlparse
else:
    import urllib.parse as urlparse
