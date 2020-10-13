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
    winkb = Gtk.RadioMenuItem(label='Windows')
    mackb = Gtk.RadioMenuItem(label='Apple',group=winkb)
    chromekb = Gtk.RadioMenuItem(label='Chromebook',group=winkb)
    ibmkb = Gtk.RadioMenuItem(label='IBM (No Super/Win key)',group=winkb)
    winmackb = Gtk.RadioMenuItem(label='Windows & Apple*',group=winkb)
    rightmod =  Gtk.CheckButton('AltGr on Right Cmd')
    vsc2st3 = Gtk.CheckButton('ST3 hotkeys for VS Code')
    caps2esc = Gtk.CheckButton('Capslock is Escape when tapped, Cmd when held')
    caps2cmd = Gtk.CheckButton('Capslock is Cmd')
    button_config = Gtk.MenuItem('Edit Config')
    # Keyboard type set below
    button_syskb = Gtk.MenuItem('System Shortcuts')
    button_region = Gtk.MenuItem('Change Language')
    button_support = Gtk.MenuItem('Support')
    global restartsvc

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

        res = subprocess.Popen(['sudo', 'systemctl','is-active','--quiet','xkeysnail'])
        res.wait()
        time.sleep(5)
        
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
        ismac = "perl -ne 'print if /^(\s{4})((?!#).*)(# Mac\n)/' ~/.config/kinto/kinto.py | wc -l"
        iswin = "perl -ne 'print if /^(\s{4})(# -- Default Win)/' ~/.config/kinto/kinto.py | wc -l"
        ischrome = "perl -ne 'print if /^(\s{4})((?!#).*)(# Chromebook\n)/' ~/.config/kinto/kinto.py | wc -l"
        iswinmac = "perl -ne 'print if /^(\s{4})(# -- Default Mac)/' ~/.config/kinto/kinto.py | wc -l"
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

        self.tweaks.connect('activate',self.setTweaks)

        self.menu.append(self.tweaks)

        # Edit Config
        self.button_config.connect('activate',self.setConfig)
        self.menu.append(self.button_config)

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

        # Check AltGr - commented out is enabled
        is_rightmod = "perl -ne 'print if /^(\s{4})(Key.*)(Multi-language)/' ~/.config/kinto/kinto.py | wc -l"
        rightmod_result = int(self.queryConfig(is_rightmod))

        # Sublime enabled for vscode
        is_vsc2st3 = "perl -ne 'print if /^(\s{4}\w.*)(- Sublime)/' ~/.config/kinto/kinto.py | wc -l"
        vsc2st3_result = int(self.queryConfig(is_vsc2st3))

        # Caps2Esc enabled
        is_caps2esc = "perl -ne 'print if /^(\s{4}{\w.*)(# Caps2Esc)/' ~/.config/kinto/kinto.py | wc -l"
        caps2esc_result = int(self.queryConfig(is_caps2esc))

        # Caps2Cmd enabled
        is_caps2cmd = "perl -ne 'print if /^(\s{4}\w.*)(# Caps2Cmd)/' ~/.config/kinto/kinto.py | wc -l"
        caps2cmd_result = int(self.queryConfig(is_caps2cmd))

        # Enter2Cmd enabled
        # (\s{4}{\w.*)(# Enter2Cmd)

        vbox = Gtk.VBox()

        self.lbl = Gtk.Label()
        global restartsvc 
        restartsvc = False
        self.rightmod =  Gtk.CheckButton('AltGr on Right Cmd')
        self.vsc2st3 = Gtk.CheckButton('ST3 hotkeys for VS Code')
        self.caps2esc = Gtk.CheckButton('Capslock is Escape when tapped, Cmd when held')
        self.caps2cmd = Gtk.CheckButton('Capslock is Cmd')
        
        if rightmod_result == 0:
            self.rightmod.set_active(True)

        if vsc2st3_result > 0:
            self.vsc2st3.set_active(True)

        if caps2esc_result > 0:
            self.caps2esc.set_active(True)
            self.caps2cmd.set_sensitive(False)

        if caps2cmd_result > 0:
            self.caps2cmd.set_active(True)
            self.caps2esc.set_sensitive(False)

        self.rightmod.signal_id = self.rightmod.connect('toggled',self.setRightMod)
        self.vsc2st3.signal_id = self.vsc2st3.connect('toggled',self.setVSC2ST3)
        self.caps2esc.signal_id = self.caps2esc.connect('toggled',self.setCaps2Esc)
        self.caps2cmd.signal_id = self.caps2cmd.connect('toggled',self.setCaps2Cmd)

        vbox.add(self.rightmod)
        vbox.add(self.vsc2st3)
        vbox.add(self.caps2esc)
        vbox.add(self.caps2cmd)
        vbox.add(self.lbl)
        win.add(vbox)

        win.show_all()

        win.connect('delete-event', self.on_delete_event)

        return

    __gsignals__ = {
        "delete-event" : "override"
    }

    def on_delete_event(event, self, widget):
        global restartsvc 
        if restartsvc == True:
            try:
                restartcmd = ['sudo', 'systemctl','restart','xkeysnail']
                subprocess.Popen(restartcmd)
                restartsvc = False

            except subprocess.CalledProcessError:
                subprocess.Popen(['notify-send','Kinto: Error restarting Kinto after setting tweaks!','-i','budgie-desktop-symbolic'])

        self.hide()
        self.destroy()
        return True

    def setRightMod(self,button):
        global restartsvc 
        try:
            if self.winkb.get_active() or self.winmackb.get_active():
                # print('winkb true')
                setkb = 's/^(\s{4})((# )(.*)(# )(WinMac - Multi-language.*)|(K)(.*)(# )(WinMac - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.mackb.get_active():
                # print('mackb true')
                setkb = 's/^(\s{4})((# )(.*)(# )(Mac - Multi-language.*)|(K)(.*)(# )(Mac - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.chromekb.get_active():
                # print('chromekb true')
                setkb = 's/^(\s{4})((# )(.*)(# )(Chromebook - Multi-language.*)|(K)(.*)(# )(Chromebook - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.ibmkb.get_active():
                # print('ibmkb true')
                setkb = 's/^(\s{4})((# )(.*)(# )(IBM - Multi-language.*)|(K)(.*)(# )(IBM - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'

            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            cmdsTerm = subprocess.Popen(cmds)

            restartsvc = True

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error Resetting AltGr!','-i','budgie-desktop-symbolic'])

        return

    def setVSC2ST3(self,button):
        global restartsvc 

        try:
            if self.chromekb.get_active() or self.ibmkb.get_active():
                setkb = 's/^(\s{4})(\w.*)(# )(Chromebook/IBM - Sublime)|^(\s{4})(# )(\w.*)(# Chromebook/IBM - Sublime)/$5$7$8$1$3$2$3$4/g'
            else:
                setkb = 's/^(\s{4})(\w.*)(# )(Default - Sublime)|^(\s{4})(# )(\w.*)(# Default - Sublime)/$5$7$8$1$3$2$3$4/g'

            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            cmdsTerm = subprocess.Popen(cmds)

            restartsvc = True

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error Resetting SublimeText remaps for VSCode!','-i','budgie-desktop-symbolic'])
        return

    def setCaps2Esc(self,button):

        global restartsvc
        try:
            if self.winkb.get_active() or self.winmackb.get_active() or self.ibmkb.get_active() or self.mackb.get_active():
                setkb = 's/^(\s{4})((# )(\{\w.*)(# Caps2Esc\n)|(\{\w.*)(# )(Caps2Esc - Chrome.*)|(\{.*)(# )(Caps2Esc\n|Placeholder)|(\w.*)(# )(Caps2Cmd.*)|(# )(\{.*)(# )(Placeholder))/    $4$5$7$6$7$8$10$9$10$11$13$12$13$14$16$17$18/g'
            if self.chromekb.get_active():
                setkb = 's/^(\s{4})((# )(\{\w.*)(# Caps2Esc - Chrome.*)|(\{\w.*)(# )(Caps2Esc\n)|(\{.*)(# )(Caps2Esc - Chrome.*|Placeholder)|(\w.*)(# )(Caps2Cmd.*)|(# )(\{.*)(# )(Placeholder))/    $4$5$7$6$7$8$10$9$10$11$13$12$13$14$16$17$18/g'

            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            if self.caps2esc.get_active():
                self.caps2cmd.set_sensitive(False)
            else:
                self.caps2cmd.set_sensitive(True)

            cmdsTerm = subprocess.Popen(cmds)

            restartsvc = True

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error resetting caps2esc!','-i','budgie-desktop-symbolic'])

        return

    def setCaps2Cmd(self,button):

        global restartsvc

        try:
            if self.winkb.get_active() or self.winmackb.get_active() or self.ibmkb.get_active() or self.mackb.get_active():
                setkb = 's/^(\s{4})((\w.*)(# )(Caps2Cmd\n)|(\w.*)(# )(Caps2Cmd - Chrome.*)|(# )(\w.*)(# )(Caps2Cmd\n)|(\{\w.*)(# )(Caps2Esc.*)|(# )(\{.*)(# )(Placeholder))/    $4$3$4$5$7$6$7$8$10$11$12$14$13$14$15$17$18$19/g'
            if self.chromekb.get_active():
                setkb = 's/^(\s{4})((\w.*)(# )(Caps2Cmd - Chrome.*)|(\w.*)(# )(Caps2Cmd\n)|(# )(\w.*)(# )(Caps2Cmd - Chrome.*)|(\{\w.*)(# )(Caps2Esc.*)|(# )(\{.*)(# )(Placeholder))/    $4$3$4$5$7$6$7$8$10$11$12$14$13$14$15$17$18$19/g'

            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            if self.caps2cmd.get_active():
                self.caps2esc.set_sensitive(False)
            else:
                self.caps2esc.set_sensitive(True)

            cmdsTerm = subprocess.Popen(cmds)

            restartsvc = True

        except subprocess.CalledProcessError:
            subprocess.Popen(['notify-send','Kinto: Error resetting caps2cmd!','-i','budgie-desktop-symbolic'])

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
            elif which(mousepad) is not None:
                subprocess.Popen(['mousepad',self.homedir+'/.config/kinto/kinto.py'])

        except subprocess.CalledProcessError:                                  # Notify user about error on running restart commands.
            subprocess.Popen(['notify-send','Kinto: Error could not open config file!','-i','budgie-desktop-symbolic'])

    def setKB(self,button,kbtype):
        try:
            if kbtype == "win":
                setkb = 's/^(\s{3})(\s{1}#)(.*# WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)( Default Win)|^(\s{3})(\s{1}# )(-)(- Default Mac*)/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$21$21$22$24$26/g'
            elif kbtype == "winmac":
                setkb = 's/^(\s{3})(\s{1}#)(.*# WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)( Default Mac.*)|^(\s{3})(\s{1}# )(-)(- Default Win)/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$21$21$22$24$26/g'
                if os.path.isfile('/sys/module/hid_apple/parameters/swap_opt_cmd'):
                    with open('/sys/module/applespi/parameters/swap_opt_cmd', 'r') as ocval:
                        optcmd = ocval.read().replace('\n', '')
                    if optcmd == '0':
                        # print("found hid_apple")
                        self.queryConfig("echo '1' | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd;echo 'options hid_apple swap_opt_cmd=1' | sudo tee /etc/modprobe.d/hid_apple.conf;sudo update-initramfs -u -k all")
                if os.path.isfile('/sys/module/applespi/parameters/swap_opt_cmd'):
                    with open('/sys/module/applespi/parameters/swap_opt_cmd', 'r') as ocval:
                        optcmd = ocval.read().replace('\n', '')
                    if optcmd == '0':
                        # print("found applespi")
                        self.queryConfig("echo '1' | sudo tee /sys/module/applespi/parameters/swap_opt_cmd;echo 'options applespi swap_opt_cmd=1' | sudo tee /etc/modprobe.d/applespi.conf;sudo update-initramfs -u -k all")
            elif kbtype == "mac":
                if os.path.isfile('/sys/module/hid_apple/parameters/swap_opt_cmd'):
                    with open('/sys/module/hid_apple/parameters/swap_opt_cmd', 'r') as ocval:
                        optcmd = ocval.read().replace('\n', '')
                    if optcmd == '1':
                        # print("found hid_apple - remove")
                        self.queryConfig("echo '0' | sudo tee /sys/module/hid_apple/parameters/swap_opt_cmd;echo 'options hid_apple swap_opt_cmd=0' | sudo tee /etc/modprobe.d/hid_apple.conf;sudo update-initramfs -u -k all")
                if os.path.isfile('/sys/module/applespi/parameters/swap_opt_cmd'):
                    with open('/sys/module/applespi/parameters/swap_opt_cmd', 'r') as ocval:
                        optcmd = ocval.read().replace('\n', '')
                    if optcmd == '1':
                        # print("found applespi - remove")
                        self.queryConfig("echo '0' | sudo tee /sys/module/applespi/parameters/swap_opt_cmd;echo 'options applespi swap_opt_cmd=0' | sudo tee /etc/modprobe.d/applespi.conf;sudo update-initramfs -u -k all")
                setkb = 's/^(\s{3})(\s{1}#)(.*# Mac\n|.*# Mac -)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)(- Default (Win|Mac.*))/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$22/g'
            elif kbtype == "chrome":
                setkb = 's/^(\s{3})(\s{1}#)(.*# Chromebook.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(\s{3})(\s{1}# )(-)(- Default (Win|Mac.*))/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$22/g'
            elif kbtype == "ibm":
                setkb ='s/^(\s{3})(\s{1}#)(.*# IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)(- Default (Win|Mac.*))/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$22/g'

            restart = ['sudo', 'systemctl','restart','xkeysnail']
            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            cmdsTerm = subprocess.Popen(cmds)
            cmdsTerm.wait()

            subprocess.Popen(restart)

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
