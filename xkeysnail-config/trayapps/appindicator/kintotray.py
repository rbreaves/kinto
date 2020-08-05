#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

import signal,subprocess,time,os
from shutil import which
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'Kinto'

class Indicator():

    homedir = os.path.expanduser("~")
    kconfig = homedir+"/.config/kinto/kinto.py"
    ostype = os.environ.get('XDG_CURRENT_DESKTOP')

    enable_id = 0
    winmac_id = 0
    chkautostart_id = 0
    autostart_bool = False
    menu = Gtk.Menu()
    checkbox_autostart = Gtk.CheckMenuItem('Autostart')
    checkbox_enable = Gtk.CheckMenuItem('Kinto Enabled')
    button_config = Gtk.MenuItem('Edit Config')
    # Keyboard type set below
    button_syskb = Gtk.MenuItem('System Shortcuts')
    button_region = Gtk.MenuItem('Change Language')

    def __init__(self):
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.homedir+'/.config/kinto/kinto-invert.svg', appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)

    def build_menu(self):

        with open(self.kconfig) as configfile:
            autostart_line = configfile.read().split('\n')[1]

        # Autostart
        if "autostart = true" in autostart_line.casefold():
            autostart_bool = True

        if autostart_bool:
            subprocess.Popen(['sudo', 'systemctl','restart','xkeysnail'])
            self.checkbox_autostart.set_active(True)
            self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,False)
        else:
            self.checkbox_autostart.set_active(False)
            self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,True)
        self.menu.append(self.checkbox_autostart)

        # Kinto Enable
        time.sleep(5)
        # sudo systemctl is-active --quiet xkeysnail
        res = subprocess.Popen(['sudo', 'systemctl','is-active','--quiet','xkeysnail'])
        res.wait()
        
        self.checkbox_enable.set_label("Kinto Enabled")

        if res.returncode == 0:
            self.checkbox_enable.set_active(True)
            self.indicator.set_icon(self.homedir+'/.config/kinto/kinto-invert.svg')
            self.enable_id = self.checkbox_enable.connect('activate',self.setEnable,False)
        else:
            self.checkbox_enable.set_active(False)
            self.indicator.set_icon(self.homedir+'/.config/kinto/kinto-color.svg')
            self.enable_id = self.checkbox_enable.connect('activate',self.setEnable,True)
        self.menu.append(self.checkbox_enable)

        # Edit Config
        self.button_config.connect('activate',self.setConfig)
        self.menu.append(self.button_config)

        # Set Keyboard Type
        command = "perl -ne 'print if /(#.*)(# Mac)\n/' ~/.config/kinto/kinto.py | wc -l"
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        res.wait()
        res = res.communicate()[0]

        if res:
            self.button_winmac = Gtk.MenuItem('Set Win/Mac KB Type')
            self.winmac_id = self.button_winmac.connect('activate',self.setKB,"winmac")
        else:
            self.button_winmac = Gtk.MenuItem('Set Mac Only KB Type')
            self.winmac_id = button_winmac.connect('activate',self.setKB,"mac")
        self.menu.append(self.button_winmac)

        # Set System Keyboard Shortcuts
        self.button_syskb.connect('activate',self.setSysKB)
        self.menu.append(self.button_syskb)

        # Set Language
        self.button_region.connect('activate',self.setRegion)
        self.menu.append(self.button_region)

        # item_quit = Gtk.MenuItem('Quit')
        # item_quit.connect('activate', quit)
        # menu.append(item_quit)
        self.menu.show_all()

        return self.menu

    def setEnable(self,button,enableKinto):
        try:
            if enableKinto:
                subprocess.Popen(['sudo', 'systemctl','restart','xkeysnail'])
                self.checkbox_enable.set_active(True)
                self.checkbox_enable.disconnect(self.enable_id)
                self.enable_id = self.checkbox_enable.connect('activate',self.setEnable,False)
                self.indicator.set_icon(self.homedir+'/.config/kinto/kinto-invert.svg')

            else:
                subprocess.Popen(['sudo', 'systemctl','stop','xkeysnail'])
                self.checkbox_enable.set_active(False)
                self.checkbox_enable.disconnect(self.enable_id)
                self.enable_id = self.checkbox_enable.connect('activate',self.setEnable,True)
                self.indicator.set_icon(self.homedir+'/.config/kinto/kinto-color.svg')

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error enabling!','-i','budgie-desktop-symbolic'])

    def setAutostart(self,button,autostart):
        try:
            if autostart == False:
                subprocess.Popen(['perl','-pi','-e','s/autostart = true/autostart = false/g',self.homedir+'/.config/kinto/kinto.py'])
                self.checkbox_autostart.set_active(False)
                self.checkbox_autostart.disconnect(self.chkautostart_id)
                self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,True)
            else:
                subprocess.Popen(['perl','-pi','-e','s/autostart = false/autostart = true/g',self.homedir+'/.config/kinto/kinto.py'])
                self.checkbox_autostart.set_active(True)
                self.checkbox_autostart.disconnect(self.chkautostart_id)
                self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,False)

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error setting autostart!','-i','budgie-desktop-symbolic'])

    def setConfig(self,button):
        try:
            if os.path.exists('/opt/sublime_text/sublime_text'):
                subprocess.Popen(['/opt/sublime_text/sublime_text',self.homedir+'/.config/kinto/kinto.py'])
            elif which(gedit) is not None:
                subprocess.Popen(['gedit',self.homedir+'/.config/kinto/kinto.py'])

        except subprocess.CalledProcessError:                                  # Notify user about error on running restart commands.
            subprocess.Popen(['notify-send','Kinto: Error could not open config file!','-i','budgie-desktop-symbolic'])

    def setKB(self,button,kbtype):
        try:
            if kbtype == "winmac":
                label = "Set Mac KB Type"
                connect = "mac"

                setwinmac = ['s/^(\s{3})(\s{1}#)(.*# WinMac\n|.*# WinMac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac\n|Mac -)/   $3$7$6$7$8/g']

            else:
                label = "Set Win/Mac KB Type"
                connect = "winmac"

                setwinmac = ['s/^(\s{3})(\s{1}#)(.*# Mac\n|.*# Mac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac)/   $3$7$6$7$8/g']

            restart = ['sudo', 'systemctl','restart','xkeysnail']
            cmds = ['perl','-pi','-e']+setwinmac+[self.kconfig]

            subprocess.Popen(cmds)

            cmdsTerm = subprocess.Popen(cmds)
            cmdsTerm.wait()

            subprocess.Popen(restart)

            self.button_winmac.set_label(label)
            self.button_winmac.disconnect(self.winmac_id)
            self.winmac_id = self.button_winmac.connect('activate',self.setKB,connect)

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error Resetting KB Type!','-i','budgie-desktop-symbolic'])

    def setSysKB(self,button):
        if self.ostype == "XFCE":
            subprocess.Popen(['xfce4-keyboard-settings'])
        else:
            subprocess.Popen(['gnome-control-center','keyboard'])

    def setRegion(self,button):
        if self.ostype == "XFCE":
            subprocess.Popen(['xfce4-keyboard-settings'])
        else:
            subprocess.Popen(['gnome-language-selector'])

    def quit(source):
        Gtk.main_quit()

Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
