# -*- coding: utf-8 -*-
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerwidget import E2iPlayerWidget
from Plugins.Extensions.IPTVPlayer.components.iptvconfigmenu import ConfigMenu
from Plugins.Extensions.IPTVPlayer.components.iptvpin import IPTVPinWidget
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import IsExecutable, IsWebInterfaceModuleAvailable
###################################################

###################################################
# FOREIGN import
###################################################
from enigma import getDesktop
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Tools.BoundFunction import boundFunction
from Components.config import config
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
###################################################
import os
####################################################
# Wywołanie wtyczki w roznych miejscach
####################################################


def Plugins(**kwargs):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        iconFile = "icons/iptvlogohd.png"
    else:
        iconFile = "icons/iptvlogo.png"
    desc = _("Watch Videos Online")
    list = []
    if config.plugins.iptvplayer.plugin_autostart.value:
        if config.plugins.iptvplayer.plugin_autostart_method.value == 'wizard':
            list.append(PluginDescriptor(name=(("E2iPlayer")), description=desc, where=[PluginDescriptor.WHERE_WIZARD], fnc=(9, pluginAutostart), needsRestart=False))
        elif config.plugins.iptvplayer.plugin_autostart_method.value == 'infobar':
            list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=pluginAutostartSetup))

    list.append(PluginDescriptor(name=(("E2iPlayer")), description=desc, where=[PluginDescriptor.WHERE_PLUGINMENU], icon=iconFile, fnc=main)) # always show in plugin menu
    list.append(PluginDescriptor(name=(("E2iPlayer")), description=desc, where=PluginDescriptor.WHERE_MENU, fnc=startIPTVfromMenu))
    if config.plugins.iptvplayer.showinextensions.value:
        list.append(PluginDescriptor(name=(("E2iPlayer")), description=desc, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
    if IsWebInterfaceModuleAvailable() and config.plugins.iptvplayer.IPTVWebIterface.value:
        try:
            list.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart, needsRestart=False)) # activating IPTV web interface
        except Exception:
            print("IPTVplayer Exception appending PluginDescriptor.WHERE_SESSIONSTART descriptor.")
    return list


######################################################
# Autostart from InfoBar - trick
######################################################
gInfoBar__init__ = None


def InfoBar__init__wrapper(self, *args, **kwargs):
    global gInfoBar__init__
    gInfoBar__init__(self, *args, **kwargs)
    self.onShow.append(doPluginAutostart)


def pluginAutostartSetup(reason, **kwargs):
    global gInfoBar__init__
    if reason == 0 and gInfoBar__init__ == None:
        from Screens.InfoBar import InfoBar
        gInfoBar__init__ = InfoBar.__init__
        InfoBar.__init__ = InfoBar__init__wrapper


def doPluginAutostart():
    from Screens.InfoBar import InfoBar
    InfoBar.instance.onShow.remove(doPluginAutostart)
    doRunMain(InfoBar.instance.session)
######################################################

####################################################
# Konfiguracja wtyczki
####################################################

#from __init__ import _


def startIPTVfromMenu(menuid, **kwargs):
    if menuid == "system":
        return [(_("Configure %s") % 'E2iPlayer', mainSetup, "iptv_config", None)]
    elif menuid == "mainmenu" and config.plugins.iptvplayer.showinMainMenu.value == True:
        return [("E2iPlayer", main, "iptv_main", None)]
    else:
        return []


def mainSetup(session, **kwargs):
    if config.plugins.iptvplayer.configProtectedByPin.value:
        session.openWithCallback(boundFunction(pinCallback, session, runSetup), IPTVPinWidget, title=_("Enter pin"))
    else:
        runSetup(session)


def runSetup(session):
    session.open(ConfigMenu)


def main(session, **kwargs):
    if config.plugins.iptvplayer.pluginProtectedByPin.value:
        session.openWithCallback(boundFunction(pinCallback, session, doRunMain), IPTVPinWidget, title=_("Enter pin"))
    else:
        doRunMain(session)


class pluginAutostart(Screen):
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self.onShow.append(self.onStart)

    def onStart(self):
        self.onShow.remove(self.onStart)
        doRunMain(self.session, self.iptvDoRunMain)

    def iptvDoRunMain(self, session):
        session.openWithCallback(self.iptvDoClose, E2iPlayerWidget)

    def iptvDoClose(self, **kwargs):
        self.close()


def doRunMain(session):
    session.open(E2iPlayerWidget)


def pinCallback(session, callbackFun, pin=None):
    if None == pin:
        return
    if pin != config.plugins.iptvplayer.pin.value:
        session.open(MessageBox, _("Pin incorrect!"), type=MessageBox.TYPE_INFO, timeout=5)
        return
    callbackFun(session)


def sessionstart(reason, **kwargs):
    if reason == 0 and 'session' in kwargs:
        try:
            import Plugins.Extensions.IPTVPlayer.Web.initiator
        except Exception as e:
            print("EXCEPTION initiating IPTVplayer WebComponent:", str(e))
