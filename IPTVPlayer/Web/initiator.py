# -*- coding: utf-8 -*-
import os
from Plugins.Extensions.OpenWebif.WebChilds.Toplevel import addExternalChild
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, isPluginInstalled
from Tools.PyVerHelper import getPyExt
from webSite import StartPage, redirectionPage, hostsPage, useHostPage, downloaderPage, settingsPage, logsPage, searchPage
from twisted.web import static

from Plugins.Extensions.IPTVPlayer.tools.iptvtools import GetPluginDir
import settings

IPTVwebRoot = static.File(GetPluginDir('Web/')) #webRoot = pluginDir to get access to icons and logos
IPTVwebRoot.putChild("icons", static.File(GetPluginDir('icons/')))
IPTVwebRoot.putChild("", StartPage())
IPTVwebRoot.putChild("hosts", hostsPage())
IPTVwebRoot.putChild("usehost", useHostPage())
IPTVwebRoot.putChild("downloader", downloaderPage())
IPTVwebRoot.putChild("settings", settingsPage())
IPTVwebRoot.putChild("logs", logsPage())
IPTVwebRoot.putChild("search", searchPage())

PyExt = getPyExt()


def checkForFC():
    ret = False
    if os.path.exists(resolveFilename(SCOPE_PLUGINS, 'Extensions/OpenWebif/controllers/base.%s' % PyExt)):
        myfileName = resolveFilename(SCOPE_PLUGINS, 'Extensions/OpenWebif/controllers/base.%s' % PyExt)
    else:
        return False

    try:
        with open(myfileName, "r") as myfile:
            data = myfile.read()
            myfile.close()
        if data.find('fancontrol') > 0 and data.find('iptvplayer') < 0:
            ret = True
            data = None
    except Exception:
        pass

    data = None
    return ret


if isPluginInstalled("OpenWebif"):
    # Old openwebif version (prior July the 14th 2017) has a bug and does not populate links to all properly registered web addons except fancontrol
    # see: https://github.com/E2OpenPlugins/e2openplugin-OpenWebif/pull/629
    #  A HACK: we will canibalize fancontrol entry point (if not installed) to present IPTVplayer option on the web
    if checkForFC() == True and not os.path.exists(resolveFilename(SCOPE_PLUGINS, 'Extensions/FanControl2/FC2webSite.%s' % PyEx)):
        fcRoot = static.File(GetPluginDir('Web/'))
        fcRoot.putChild("", redirectionPage())
        try:
            addExternalChild(("fancontrol", fcRoot, "E2iPlayer", settings.WebInterfaceVersion))
            addExternalChild(("iptvplayer", IPTVwebRoot, None, None))
        except Exception:
            print("[E2iPlayer] exception registering Web interface in FC mode")
    else: #user still can use IPTV web interface, but would need to mark URL manually depending on the openWebIf version
        try:
            addExternalChild(("iptvplayer", IPTVwebRoot, "E2iPlayer", settings.WebInterfaceVersion))
            addExternalChild(("e2iplayer", IPTVwebRoot, "E2iPlayer", settings.WebInterfaceVersion))
        except Exception:
            print("[E2iPlayer] exception registering Web interface in NATIVE mode")
else:
    print("No known webinterface available")
