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
    menukb = Gtk.Menu()
    tweaks = Gtk.MenuItem('Tweaks')
    checkbox_autostart = Gtk.CheckMenuItem('Autostart')
    checkbox_enable = Gtk.CheckMenuItem('Kinto Enabled')
    keyboards = Gtk.MenuItem('Keyboard Types')
    keyboards.set_submenu(menukb)
    winkb = Gtk.CheckMenuItem('Windows')
    mackb = Gtk.CheckMenuItem('Apple')
    chromekb = Gtk.CheckMenuItem('Chromebook')
    ibmkb = Gtk.CheckMenuItem('IBM (No Super/Win key)')
    winmackb = Gtk.CheckMenuItem('Windows & Apple*')
    button_config = Gtk.MenuItem('Edit Config')
    # Keyboard type set below
    button_syskb = Gtk.MenuItem('System Shortcuts')
    button_region = Gtk.MenuItem('Change Language')
    button_support = Gtk.MenuItem('Support')

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
        # time.sleep(5)
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

        # Keyboard Types
        # self.keyboards.connect('activate',self.setConfig)
        ismac = "perl -ne 'print if /^(\s{4})((?!#).*)(# Mac\n)/' ~/.config/kinto/kinto.py | wc -l"
        iswin = "perl -ne 'print if /^(\s{4})((?!#).*)(# Win\n)/' ~/.config/kinto/kinto.py | wc -l"
        ischrome = "perl -ne 'print if /^(\s{4})((?!#).*)(# Chromebook\n)/' ~/.config/kinto/kinto.py | wc -l"
        iswinmac = "perl -ne 'print if /^(\s{4})((?!#).*)(# WinMac\n)/' ~/.config/kinto/kinto.py | wc -l"
        isibm = "perl -ne 'print if /^(\s{4})((?!#).*)(# IBM\n)/' ~/.config/kinto/kinto.py | wc -l"
        mac_result = int(self.queryConfig(ismac))
        win_result = int(self.queryConfig(iswin))
        chrome_result = int(self.queryConfig(ischrome))
        ibm_result = int(self.queryConfig(isibm))
        winmac_result = int(self.queryConfig(iswinmac))

        countkb = 0

        if mac_result:
            self.mackb.set_active(True)
            countkb += 1
        if win_result:
            self.winkb.set_active(True)
            countkb += 1
        if chrome_result:
            self.chromekb.set_active(True)
            countkb += 1
        if winmac_result:
            self.winmackb.set_active(True)
            countkb += 1
        if ibm_result:
            self.ibmkb.set_active(True)
            countkb += 1

        if countkb > 1:
            subprocess.Popen(['notify-send','Kinto: Remove ' + str(countkb-1) + ' kb type(s)','-i','budgie-desktop-symbolic'])

        self.mackb.signal_id = self.mackb.connect('activate',self.setKB,"mac")
        self.winkb.signal_id = self.winkb.connect('activate',self.setKB,"win")
        self.chromekb.signal_id = self.chromekb.connect('activate',self.setKB,"chrome")
        self.ibmkb.signal_id = self.ibmkb.connect('activate',self.setKB,"ibm")
        self.winmackb.signal_id = self.winmackb.connect('activate',self.setKB,"winmac")

        self.menukb.append(self.winkb)
        self.menukb.append(self.mackb)
        self.menukb.append(self.chromekb)
        self.menukb.append(self.ibmkb)
        self.menukb.append(self.winmackb)

        self.menu.append(self.keyboards)

        # Keyboard tweaks
        # self.menu_tweaks.append(self.rightmod)
        # self.menu_tweaks.append(self.vsc2st3)

        self.tweaks.connect('activate',self.setTweaks)

        self.menu.append(self.tweaks)

        # Edit Config
        self.button_config.connect('activate',self.setConfig)
        self.menu.append(self.button_config)

        # Set Keyboard Type
        # command = "perl -ne 'print if /(#.*)(# Mac)\n/' ~/.config/kinto/kinto.py | wc -l"
        # res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
        # res.wait()
        # res = res.communicate()[0]

        # if res:
        #     self.button_winmac = Gtk.MenuItem('Set Win/Mac KB Type')
        #     self.winmac_id = self.button_winmac.connect('activate',self.setKB,"winmac")
        # else:
        #     self.button_winmac = Gtk.MenuItem('Set Mac Only KB Type')
        #     self.winmac_id = button_winmac.connect('activate',self.setKB,"mac")
        # self.menu.append(self.button_winmac)

        # Set System Keyboard Shortcuts
        self.button_syskb.connect('activate',self.setSysKB)
        self.menu.append(self.button_syskb)

        # Set Language
        self.button_region.connect('activate',self.setRegion)
        self.menu.append(self.button_region)

        item_quit = Gtk.MenuItem('Close')
        item_quit.connect('activate', quit)
        self.menu.append(item_quit)
        self.menu.show_all()

        return self.menu

    def setTweaks(self,button):
        win = Gtk.Window()
        win.set_title("Kinto Tweaks")
        win.set_default_size(350, 200)
        win.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.VBox()

        self.lbl = Gtk.Label()
        self.rightmod =  Gtk.CheckButton('AltGr on Right Cmd')
        self.vsc2st3 = Gtk.CheckButton('ST3 hotkeys for VS Code')
        self.caps2esc = Gtk.CheckButton('Capslock is Escape when tapped, Cmd when held')
        self.caps2cmd = Gtk.CheckButton('Capslock is Cmd')
        self.rightmod.connect('toggled',self.setRightMod)
        self.vsc2st3.connect('toggled',self.setVSC2ST3)
        self.caps2esc.connect('toggled',self.setCaps2Esc)
        self.caps2cmd.connect('toggled',self.setCaps2Cmd)
        vbox.add(self.rightmod)
        vbox.add(self.vsc2st3)
        vbox.add(self.caps2esc)
        vbox.add(self.caps2cmd)
        vbox.add(self.lbl)
        win.add(vbox)

        win.show_all()
        return

    def setRightMod(self,button):
        return

    def setVSC2ST3(self,button):
        return

    def setCaps2Esc(self,button):
        return

    def setCaps2Cmd(self,button):
        return

    def queryConfig(self,query):
        res = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=None, shell=True)
        res.wait()
        return res.communicate()[0].strip().decode('UTF-8')

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
            set_mackb = False
            set_winkb = False
            set_chromekb = False
            set_ibmkb = False
            set_winmackb = False

            if kbtype == "win":
                if not self.winkb.get_active():
                    if not self.winmackb.get_active():
                        print("run query to undo win/winmac")
                    return

                set_winkb = True

                setkb = ['s/^(\s{3})(\s{1}#)(.*# WinMac\n|.*# WinMac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac\n|Mac -)/   $3$7$6$7$8/g']
            elif kbtype == "winmac":
                if not self.winmackb.get_active():
                    return

                set_winmackb = True

                setkb = ['s/^(\s{3})(\s{1}#)(.*# WinMac\n|.*# WinMac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac\n|Mac -)/   $3$7$6$7$8/g']
                if os.path.isfile('/sys/module/e1000/version'):
                    print("found file")
                if os.path.isfile('/sys/module/hid_apple/parameters/swap_opt_cmd'):
                    print("found file 1")
                if os.path.isfile('/sys/module/applespi/parameters/swap_opt_cmd'):
                    print("found file 2")
            elif kbtype == "mac":
                if not self.mackb.get_active():
                    return

                set_mackb = True

                setkb = ['s/^(\s{3})(\s{1}#)(.*# Mac\n|.*# Mac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac)/   $3$7$6$7$8/g']
            elif kbtype == "chrome":
                if not self.chromekb.get_active():
                    return

                set_chromekb = True
            elif kbtype == "ibm":
                if not self.ibmkb.get_active():
                    return

                set_ibmkb = True

            self.mackb.disconnect(self.mackb.signal_id)
            self.winkb.disconnect(self.winkb.signal_id)
            self.chromekb.disconnect(self.chromekb.signal_id)
            self.ibmkb.disconnect(self.ibmkb.signal_id)
            self.winmackb.disconnect(self.winmackb.signal_id)

            self.winkb.set_active(set_winkb)
            self.mackb.set_active(set_mackb)
            self.chromekb.set_active(set_chromekb)
            self.ibmkb.set_active(set_ibmkb)
            self.winmackb.set_active(set_winmackb)

            self.mackb.signal_id = self.mackb.connect('activate',self.setKB,"mac")
            self.winkb.signal_id = self.winkb.connect('activate',self.setKB,"win")
            self.chromekb.signal_id = self.chromekb.connect('activate',self.setKB,"chrome")
            self.ibmkb.signal_id = self.ibmkb.connect('activate',self.setKB,"ibm")
            self.winmackb.signal_id = self.winkb.connect('activate',self.setKB,"winmac")

            # setkb =
            # restart = ['sudo', 'systemctl','restart','xkeysnail']
            # cmds = ['perl','-pi','-e']+setkb+[self.kconfig]

            # subprocess.Popen(cmds)

            # cmdsTerm = subprocess.Popen(cmds)
            # cmdsTerm.wait()

            # subprocess.Popen(restart)

            # self.button_winmac.set_label(label)
            # self.button_winmac.disconnect(self.winmac_id)
            # self.winmac_id = self.button_winmac.connect('activate',self.setKB,connect)

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error Resetting KB Type!','-i','budgie-desktop-symbolic'])

    def setSysKB(self,button):
        if self.ostype == "XFCE":
            subprocess.Popen(['xfce4-keyboard-settings'])
        else:
            subprocess.Popen(['gnome-control-center','keyboard'])

    def setRegion(self,button):
        if self.ostype == "XFCE":
            subprocess.Popen(['gnome-language-selector'])
        else:
            subprocess.Popen(['gnome-control-center','region'])

    def quit(source):
        Gtk.main_quit()

Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
