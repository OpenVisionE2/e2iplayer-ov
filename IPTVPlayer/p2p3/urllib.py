from Plugins.Extensions.IPTVPlayer.p2p3.pVer import isPY2

if isPY2():
    from urllib2 import HTTPRedirectHandler, BaseHandler, HTTPHandler, HTTPError, URLError, build_opener, urlopen, HTTPCookieProcessor, HTTPSHandler, ProxyHandler, Request
    from urllib import addinfourl, quote_plus, unquote, urlencode, quote
    from Plugins.Extensions.IPTVPlayer.p2p3.urlparse import urljoin, urlparse, urlunparse
else:
    from urllib.request import urlopen, build_opener, HTTPRedirectHandler, addinfourl, HTTPHandler, HTTPSHandler, BaseHandler, HTTPCookieProcessor, ProxyHandler, Request
    from urllib.parse import quote_plus, unquote, urlencode, quote
    from urllib.error import URLError, HTTPError
    from urllib.parse import urljoin, urlparse, urlunparse
