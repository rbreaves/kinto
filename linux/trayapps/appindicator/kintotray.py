#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

import signal,time,os,fcntl,datetime,re
from subprocess import Popen, PIPE, CalledProcessError
from shutil import which
from gi.repository import Gtk,GLib,GdkPixbuf
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

import signal

def kill_child():
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)

import atexit
atexit.register(kill_child)

APPINDICATOR_ID = 'Kinto'

class Indicator():

    global child_pid
    global sysv
    try:
        sysv = int(Popen("pidof systemd >/dev/null 2>&1 && echo '0' || echo '1'", stdout=PIPE, shell=True).communicate()[0].strip().decode('UTF-8'))
    except:
        sysv = 2
    if sysv:
        kinto_status = Popen("export TERM=xterm-color;while :; do clear; pgrep 'xkeysnail' && echo 'active'; sleep 2; done", stdout=PIPE, shell=True)
    else:
        kinto_status = Popen("export TERM=xterm-color;while :; do clear; systemctl is-active xkeysnail; sleep 2; done", stdout=PIPE, shell=True)
    child_pid = kinto_status.pid

    homedir = os.path.expanduser("~")
    kconfig = homedir+"/.config/kinto/kinto.py"
    ostype = os.environ.get('XDG_CURRENT_DESKTOP')

    enable_id = 0
    winmac_id = 0
    chkautostart_id = 0
    autostart_bool = False
    menu = Gtk.Menu()
    menukb = Gtk.Menu()
    checkbox_autostart = Gtk.CheckMenuItem(label='Autostart')
    restart = Gtk.MenuItem(label='Restart')
    stop = Gtk.MenuItem(label='Stop')
    keyboards = Gtk.MenuItem(label='Keyboard Types')
    keyboards.set_submenu(menukb)
    winkb = Gtk.RadioMenuItem(label='Windows')
    mackb = Gtk.RadioMenuItem(label='Apple',group=winkb)
    chromekb = Gtk.RadioMenuItem(label='Chromebook',group=winkb)
    ibmkb = Gtk.RadioMenuItem(label='IBM (No Super/Win key)',group=winkb)
    winmackb = Gtk.RadioMenuItem(label='Windows & Apple*',group=winkb)
    edit = Gtk.MenuItem(label='Customize')
    edit_submenu = Gtk.Menu()
    edit.set_submenu(edit_submenu)
    tweaks = Gtk.MenuItem(label='Tweaks')
    rightmod =  Gtk.CheckButton(label='AltGr on Right Cmd')
    vsc2st3 = Gtk.CheckButton(label='ST3 hotkeys for VS Code')
    caps2esc = Gtk.CheckButton(label='Capslock is Escape when tapped, Cmd when held')
    caps2cmd = Gtk.CheckButton(label='Capslock is Cmd')
    button_config = Gtk.MenuItem(label='Kinto Config (shortcuts)')
    service = Gtk.MenuItem(label='Kinto Service')
    # Keyboard type set below
    button_syskb = Gtk.MenuItem(label='System Shortcuts')
    button_region = Gtk.MenuItem(label='Change Language')
    systray = Gtk.CheckMenuItem(label='Tray Enabled')
    helpm = Gtk.MenuItem(label='Help')
    help_submenu = Gtk.Menu()
    helpm.set_submenu(help_submenu)
    debug = Gtk.MenuItem(label='Debug')
    opengui = Gtk.MenuItem(label='Open Kinto')
    support = Gtk.MenuItem(label='Support')
    about = Gtk.MenuItem(label='About')
    global restartsvc
    restartsvc = False
    unixts = int(time.time())
    last_status = ''

    def __init__(self):
        global sysv
        try:
            sysv = int(Popen("pidof systemd >/dev/null 2>&1 && echo '0' || echo '1'", stdout=PIPE, shell=True).communicate()[0].strip().decode('UTF-8'))
        except:
            sysv = 1
        if sysv:
            res = Popen(['pgrep','xkeysnail'])
        else:
            res = Popen(['sudo', 'systemctl','is-active','--quiet','xkeysnail'])
        res.wait()

        if res.returncode == 0:
            self.last_status = 'active'
            self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.environ['HOME']+'/.config/kinto/kinto-invert.svg', appindicator.IndicatorCategory.SYSTEM_SERVICES)
        else:
            self.last_status = 'inactive'
            self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.environ['HOME']+'/.config/kinto/kinto.svg', appindicator.IndicatorCategory.SYSTEM_SERVICES)

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu(res))
        notify.init(APPINDICATOR_ID)

        GLib.timeout_add(2000, self.update_terminal)

    def build_menu(self,res):

        with open(self.kconfig) as configfile:
            autostart_line = configfile.read().split('\n')[1]

        # Autostart
        if "autostart = true" in autostart_line.casefold():
            autostart_bool = True

        if autostart_bool:
            # Popen(['sudo', 'systemctl','restart','xkeysnail'])
            self.checkbox_autostart.set_active(True)
            self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,False)
        else:
            self.checkbox_autostart.set_active(False)
            self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,True)

        self.restart.connect('activate',self.runRestart)
        self.menu.append(self.restart)
        self.stop.connect('activate',self.runStop)
        self.menu.append(self.stop)

        self.refreshKB()

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
        self.edit_submenu.append(self.tweaks)
        self.button_config.connect('activate',self.setConfig)
        self.edit_submenu.append(self.button_config)
        self.service.connect('activate',self.setService)
        self.edit_submenu.append(self.service)
        # Set System Keyboard Shortcuts
        self.button_syskb.connect('activate',self.setSysKB)
        self.edit_submenu.append(self.button_syskb)
        # Set Language
        self.button_region.connect('activate',self.setRegion)
        self.edit_submenu.append(self.button_region)
        self.edit_submenu.append(self.checkbox_autostart)
        if os.path.exists(os.environ['HOME']+'/.config/autostart/kintotray.desktop'):
            self.systray.set_active(True)
            self.systray.signal_id = self.systray.connect('activate',self.checkTray,False)
        else:
            self.systray.signal_id = self.systray.connect('activate',self.checkTray,True)
        self.edit_submenu.append(self.systray)
        self.menu.append(self.edit)

        self.debug.connect('activate',self.runDebug,1)
        self.help_submenu.append(self.debug)
        self.opengui.connect('activate',self.runDebug,0)
        self.help_submenu.append(self.opengui)
        self.support.connect('activate',self.openSupport)
        self.help_submenu.append(self.support)
        self.about.connect('activate',self.runAbout)
        self.help_submenu.append(self.about)
        self.menu.append(self.helpm)

        self.keyboards.connect('activate',self.refresh)

        # self.debug.connect('activate',self.runDebug)
        # self.menu.append(self.debug)

        # self.tweaks.connect('activate',self.setTweaks)
        # self.menu.append(self.tweaks)

        # Edit Config
        # self.button_config.connect('activate',self.setConfig)
        # self.menu.append(self.button_config)

        # # Set System Keyboard Shortcuts
        # self.button_syskb.connect('activate',self.setSysKB)
        # self.menu.append(self.button_syskb)

        # # Set Language
        # self.button_region.connect('activate',self.setRegion)
        # self.menu.append(self.button_region)

        item_quit = Gtk.MenuItem(label='Close')
        item_quit.connect('activate', quit)
        self.menu.append(item_quit)
        self.menu.show_all()

        return self.menu

    # def refresh(self, widget, event):
    #     print('refresh!!!')
    #     if event.button != 1:
    #         return False  #only intercept left mouse button
    #     md = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, "herp derp, I only needed one click")
    #     md.run()
    #     md.destroy()
    #     return True

    def checkTray(self,button,tray_bool):
        # path.exists('.config/autostart/kintotray.py')
        if tray_bool:
            Popen(['cp',os.environ['HOME']+'/.config/kinto/kintotray.desktop',os.environ['HOME']+'/.config/autostart/kintotray.desktop'])
            self.systray.disconnect(self.systray.signal_id)
            self.systray.set_active(True)
            self.systray.signal_id = self.systray.connect('activate',self.checkTray,False)
        else:
            Popen(['rm',os.environ['HOME']+'/.config/autostart/kintotray.desktop'])
            Gtk.main_quit()
            self.systray.disconnect(self.systray.signal_id)
            self.systray.set_active(False)
            self.systray.signal_id = self.systray.connect('activate',self.checkTray,True)
        return

    def refresh(self,button):
        self.refreshKB()

    def refreshKB(self):
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
            ibmkb.set_active(True)
            countkb += 1

        if countkb > 1:
            Popen(['notify-send','Kinto: Remove ' + str(countkb-1) + ' kb type(s)'])

        return

    def non_block_read(self):
        ''' even in a thread, a normal read with block until the buffer is full '''
        output = self.kinto_status.stdout
        # with open('goodlines.txt') as f:
        #     mylist = list(f)
        # output = '\n'.join(self.kinto_status.stdout.splitlines()[-1:])
        # '\n'.join(stderr.splitlines()[-N:])
        # .splitlines()[-1:]
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        op = output.read()
        if op == None:
            return ''
        status = op.decode('utf-8').rstrip()
        if "inactive" in status or "failed" in status or "deactivating" in status or "activating" in status:
            stats = "inactive"
        elif "active" in status:
            stats = "active"
        else:
            stats = "inactive"
        return stats

    def update_terminal(self):
        status = self.non_block_read().strip()
        nowts = int(time.time())
        if (nowts - self.unixts) > 5 and (status=='active' and self.indicator.get_icon() != os.environ['HOME']+'/.config/kinto/kinto-invert.svg'):
            self.indicator.set_icon(os.environ['HOME']+'/.config/kinto/kinto-invert.svg')
        elif (nowts - self.unixts) > 5 and (status == 'inactive' and self.indicator.get_icon() != os.environ['HOME']+'/.config/kinto/kinto.svg'):
            self.indicator.set_icon(os.environ['HOME']+'/.config/kinto/kinto.svg')
        self.last_status = status

        return self.kinto_status.poll() is None

    def openSupport(self,button):
        Gtk.show_uri_on_window(None, "https://github.com/rbreaves/kinto#table-of-contents", Gtk.get_current_event_time())
        return

    def runAbout(self,button):
        win = Gtk.Window()

        path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
        width = -1
        height = 128
        preserve_aspect_ratio = True

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
        win.set_default_icon_list([pixbuf])

        win.set_title("About")
        win.set_default_size(350, 200)
        win.set_position(Gtk.WindowPosition.CENTER)

        context = win.get_style_context()
        default_background = str(context.get_background_color(Gtk.StateType.NORMAL))

        tokenValue = re.search('red=(\d.\d+), green=(\d.\d+), blue=(\d.\d+), alpha=(\d.\d+)', default_background)
        red = float(tokenValue.group(1))
        green = float(tokenValue.group(2))
        blue = float(tokenValue.group(3))
        alpha = float(tokenValue.group(4))

        bgAvg = (red + green + blue)/3

        if(bgAvg > 0.5):
            theme = "light"
        else:
            theme = "dark"

        vbox = Gtk.VBox()
        # innervbox = Gtk.VBox()

        if theme == "dark":
            path = os.environ['HOME']+'/.config/kinto/kinto-invert.svg'
        else:
            path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
        width = -1
        height = 128
        preserve_aspect_ratio = True

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
        image = Gtk.Image()
        image.set_from_pixbuf(pixbuf)

        with open(os.environ['HOME']+'/.config/kinto/version', 'r') as file:
            verdata = file.read().replace('\n', '')

        version = Gtk.Label('Kinto v' + verdata)

        credits = Gtk.Label("Author: Ben Reaves")
        spacer = Gtk.Label(" ")
        copy = Gtk.Label("© 2019, 2020 - GPLv2")
        url = Gtk.LinkButton("http://kinto.sh", label="kinto.sh")

        vbox.add(image)
        vbox.add(version)
        vbox.add(spacer)
        vbox.add(credits)
        vbox.add(copy)
        vbox.add(url)
        win.add(vbox)

        win.show_all()

        version.set_selectable(True)      
        win.connect('delete-event', self.on_delete_event)

        return

    def setTweaks(self,button):
        win = Gtk.Window()

        path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
        width = -1
        height = 128
        preserve_aspect_ratio = True

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
        win.set_default_icon_list([pixbuf])

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
        self.rightmod =  Gtk.CheckButton(label='AltGr on Right Cmd')
        self.vsc2st3 = Gtk.CheckButton(label='ST3 hotkeys for VS Code')
        self.caps2esc = Gtk.CheckButton(label='Capslock is Escape when tapped, Cmd when held')
        self.caps2cmd = Gtk.CheckButton(label='Capslock is Cmd')
        
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
                if sysv:
                    restartcmd = ['sudo', '-E','/etc/init.d/kinto','restart']
                else:
                    restartcmd = ['sudo', 'systemctl','restart','xkeysnail']
                Popen(restartcmd)
                restartsvc = False

            except CalledProcessError:
                Popen(['notify-send','Kinto: Error restarting Kinto after setting tweaks!'])

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

            cmdsTerm = Popen(cmds)

            restartsvc = True

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error Resetting AltGr!'])

        return

    def setVSC2ST3(self,button):
        global restartsvc 

        try:
            if self.chromekb.get_active() or self.ibmkb.get_active():
                setkb = 's/^(\s{4})(\w.*)(# )(Chromebook/IBM - Sublime)|^(\s{4})(# )(\w.*)(# Chromebook/IBM - Sublime)/$5$7$8$1$3$2$3$4/g'
            else:
                setkb = 's/^(\s{4})(\w.*)(# )(Default - Sublime)|^(\s{4})(# )(\w.*)(# Default - Sublime)/$5$7$8$1$3$2$3$4/g'

            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            cmdsTerm = Popen(cmds)

            restartsvc = True

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error Resetting SublimeText remaps for VSCode!'])
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

            cmdsTerm = Popen(cmds)

            restartsvc = True

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error resetting caps2esc!'])

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

            cmdsTerm = Popen(cmds)

            restartsvc = True

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error resetting caps2cmd!'])

        return

    def runRestart(self,button):
        global sysv
        try:
            if sysv:
                stop = Popen(['sudo', '-E','/etc/init.d/kinto','stop'])
            else:
                stop = Popen(['sudo', 'systemctl','stop','xkeysnail'])
            stop.wait()
            time.sleep(1)
            res = Popen(['pgrep','xkeysnail'])
            res.wait()

            if res.returncode == 0:
                # Popen(['notify-send','Kinto: Ending Debug'])
                pkillxkey = Popen(['sudo', 'pkill','-f','bin/xkeysnail'])
                pkillxkey.wait()
            
            if sysv:
                Popen(['sudo', '-E','/etc/init.d/kinto','start'])
            else:
                Popen(['sudo', 'systemctl','start','xkeysnail'])
        except:
            Popen(['notify-send','Kinto: Error restarting Kinto!'])

    def runStop(self,button):
        global sysv
        try:
            if sysv:
                stop = Popen(['sudo', '-E','/etc/init.d/kinto','stop'])
            else:
                stop = Popen(['sudo', 'systemctl','stop','xkeysnail'])
            stop.wait()
            time.sleep(1)
            res = Popen(['pgrep','xkeysnail'])
            res.wait()

            if res.returncode == 0:
                # Popen(['notify-send','Kinto: Ending Debug'])
                pkillxkey = Popen(['sudo', 'pkill','-f','bin/xkeysnail'])
                pkillxkey.wait()
        except:
            Popen(['notify-send','Kinto: Error stopping Kinto!'])

    def runDebug(self,button,opendebug):
        try:
            if opendebug:
                Popen([os.environ['HOME']+'/.config/kinto/gui/kinto-gui.py','-d'])
            else:
                Popen([os.environ['HOME']+'/.config/kinto/gui/kinto-gui.py'])
        except:
            Popen(['notify-send','Kinto: Error opening Kinto!'])

    def queryConfig(self,query):
        res = Popen(query, stdout=PIPE, stderr=None, shell=True)
        res.wait()
        return res.communicate()[0].strip().decode('UTF-8')

    def setAutostart(self,button,autostart):
        try:
            if autostart == False:
                Popen(['perl','-pi','-e','s/autostart = true/autostart = false/g',os.environ['HOME']+'/.config/kinto/kinto.py'])
                self.checkbox_autostart.set_active(False)
                self.checkbox_autostart.disconnect(self.chkautostart_id)
                self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,True)
            else:
                Popen(['perl','-pi','-e','s/autostart = false/autostart = true/g',os.environ['HOME']+'/.config/kinto/kinto.py'])
                self.checkbox_autostart.set_active(True)
                self.checkbox_autostart.disconnect(self.chkautostart_id)
                self.chkautostart_id = self.checkbox_autostart.connect('activate',self.setAutostart,False)

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error setting autostart!'])

    def setConfig(self,button):
        try:
            if os.path.exists('/opt/sublime_text/sublime_text'):
                Popen(['/opt/sublime_text/sublime_text',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which('gedit') is not None:
                Popen(['gedit',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which('mousepad') is not None:
                Popen(['mousepad',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which('kate') is not None:
                Popen(['kate',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which('kwrite') is not None:
                Popen(['kwrite',os.environ['HOME']+'/.config/kinto/kinto.py'])

        except CalledProcessError:                                  # Notify user about error on running restart commands.
            Popen(['notify-send','Kinto: Error could not open config file!'])

    def setService(self,button):
        try:
            if os.path.exists('/opt/sublime_text/sublime_text'):
                Popen(['/opt/sublime_text/sublime_text','/lib/systemd/system/xkeysnail.service'])
            elif which('gedit') is not None:
                Popen(['gedit','/lib/systemd/system/xkeysnail.service'])
            elif which('mousepad') is not None:
                Popen(['mousepad','/lib/systemd/system/xkeysnail.service'])
            elif which('kate') is not None:
                Popen(['kate','/lib/systemd/system/xkeysnail.service'])
            elif which('kwrite') is not None:
                Popen(['kwrite','/lib/systemd/system/xkeysnail.service'])

        except CalledProcessError:                                  # Notify user about error on running restart commands.
            Popen(['notify-send','Kinto: Error could not open config file!'])

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

            cmds = ['perl','-pi','-e',setkb,self.kconfig]
            cmdsTerm = Popen(cmds)
            cmdsTerm.wait()

            if sysv:
                restart = ['sudo', '-E','/etc/init.d/kinto','restart']
            else:
                restart = ['sudo', 'systemctl','restart','xkeysnail']
            Popen(restart)

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error Resetting KB Type!'])

    def setSysKB(self,button):
        if self.ostype == "XFCE":
            Popen(['xfce4-keyboard-settings'])
        elif self.ostype == "KDE":
            self.queryConfig('systemsettings >/dev/null 2>&1 || systemsettings5 >/dev/null 2>&1')
        else:
            Popen(['gnome-control-center','keyboard'])

    def setRegion(self,button):
        if self.ostype == "XFCE":
            Popen(['gnome-language-selector'])
        elif self.ostype == "KDE":
            self.queryConfig('kcmshell4 kcm_translations >/dev/null 2>&1 || kcmshell5 kcm_translations >/dev/null 2>&1')
        else:
            Popen(['gnome-control-center','region'])

    def quit(source):
        Gtk.main_quit()

Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
