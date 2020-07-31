#!/usr/bin/env python3

# Based on
#
# gtk-example.py
# (c) Aleksander Alekseev 2016
# http://eax.me/
#
# Additions made by Ben Reaves
# 2020
# http://kinto.sh
#

import signal
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import Notify

APPID = "kinto"
CURRDIR = os.path.dirname(os.path.abspath(__file__))
# could be PNG or SVG as well
ICON = os.path.join(CURRDIR, '../icons/kinto-invert.svg')
# ICON = Gtk.Image.new_from_icon_name("kinto-invert", Gtk.IconSize.BUTTON)

# Cross-platform tray icon implementation
# See:
# * http://ubuntuforums.org/showthread.php?t=1923373#post11902222
# * https://github.com/syncthing/syncthing-gtk/blob/master/syncthing_gtk/statusicon.py
class TrayIcon:

    def __init__(self, appid, icon, menu):
        self.menu = menu

        APPIND_SUPPORT = 1
        try:
            from gi.repository import AppIndicator3
        except:
            APPIND_SUPPORT = 0

        if APPIND_SUPPORT == 1:
            self.ind = AppIndicator3.Indicator.new(
                appid, icon,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:
            self.ind = Gtk.StatusIcon()
            self.ind.set_from_file(icon)
            self.ind.connect('popup-menu', self.onPopupMenu)

    def onPopupMenu(self, icon, button, time):
        self.menu.popup(None, None, Gtk.StatusIcon.position_menu, icon,
                        button, time)


class Handler:

    def __init__(self):
        self.window_is_hidden = False

    def onShowButtonClicked(self, button):
        msg = "Clicked: " + entry.get_text()
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, msg)
        dialog.run()
        dialog.destroy()

    def onNotify(self, *args):
        Notify.Notification.new("Notification", "Hello!", ICON).show()

    def onShowOrHide(self, *args):
        if self.window_is_hidden:
            window.show()
        else:
            window.hide()

        self.window_is_hidden = not self.window_is_hidden

    def onQuit(self, *args):
        Notify.uninit()
        Gtk.main_quit()

# Handle pressing Ctr+C properly, ignored by default
signal.signal(signal.SIGINT, signal.SIG_DFL)

builder = Gtk.Builder()
builder.add_from_file('kintonotify.glade')
builder.connect_signals(Handler())

# window = builder.get_object('window1')
# window.set_icon_from_file(ICON)
# window.show_all()

entry = builder.get_object('entry1')
menu = builder.get_object('menu1')
icon = TrayIcon(APPID, ICON, menu)
Notify.init(APPID)

Gtk.main()
