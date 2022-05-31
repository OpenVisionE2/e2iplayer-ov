from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

if isPY2():
    import cookielib
else:
    import http.cookiejar as cookielib
