#!/usr/bin/env python3

import gi,os,time,fcntl,argparse,re
import warnings
warnings.filterwarnings("ignore")
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk,Gdk,GdkPixbuf
from gi.repository import Vte,GLib
from shutil import which
from subprocess import Popen,PIPE,CalledProcessError
from distutils.util import strtobool

import signal

def kill_child():
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)

import atexit
atexit.register(kill_child)

class MyWindow(Gtk.Window):

    options = {
        "kbtype"    : "ask",
        "rightmod"  : True,
        "vsc2st3"   : False,
        "capslock"  : "default",
        "systray"   : True,
        "autostart" : True
    }

    setupwin = Gtk.Window()
    container = Gtk.Box()
    overlay = Gtk.Overlay()
    background = Gtk.Image()
    bgcaps = Gtk.Image()
    bgspace = Gtk.Image()
    bgsuccess1 = Gtk.Image()
    bgsuccess2 = Gtk.Image()
    bgsuccess3 = Gtk.Image()
    bgsuccess4 = Gtk.Image()
    bgerror = Gtk.Image()
    bguninstall = Gtk.Image()
    last_onward = Gtk.Button()
    first_onward = Gtk.ToggleButton()
    page = 1

    label = Gtk.Label()
    label.set_halign(Gtk.Align.END)
    ostype = os.environ.get('XDG_CURRENT_DESKTOP')
    global openWin
    openWin = False

    global child_pid
    global sysv
    try:
        sysv = int(Popen("pidof systemd >/dev/null 2>&1 && echo '0' || echo '1'", stdout=PIPE, shell=True).communicate()[0].strip().decode('UTF-8'))
    except:
        sysv = 2
    if sysv:
        kinto_status = Popen("while :; do clear; pgrep 'xkeysnail' && echo 'active'; sleep 2; done", stdout=PIPE, shell=True)
    else:
        kinto_status = Popen("while :; do clear; systemctl is-active xkeysnail; sleep 2; done", stdout=PIPE, shell=True)
    child_pid = kinto_status.pid

    winkb = Gtk.RadioMenuItem(label='Windows')
    mackb = Gtk.RadioMenuItem(label='Apple',group=winkb)
    chromekb = Gtk.RadioMenuItem(label='Chromebook',group=winkb)
    ibmkb = Gtk.RadioMenuItem(label='IBM (No Super/Win key)',group=winkb)
    winmackb = Gtk.RadioMenuItem(label='Windows & Apple*',group=winkb)

    mackb.signal_id = 0
    winkb.signal_id = 0
    chromekb.signal_id = 0
    ibmkb.signal_id = 0
    winmackb.signal_id = 0

    menuitem_auto = Gtk.CheckMenuItem(label="Autostart")
    menuitem_auto.signal_id = 0
    menuitem_systray = Gtk.CheckMenuItem(label="Tray Enabled")
    menuitem_systray.signal_id = 0

    def __init__(self):

        Gtk.Window.__init__(self, title="Kinto.sh")
        self.set_size_request(600, 360)

        homedir = os.path.expanduser("~")
        self.kconfig = homedir+"/.config/kinto/kinto.py"
        autostart_bool = False

        path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
        width = -1
        height = 256
        preserve_aspect_ratio = True

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
        self.set_default_icon_list([pixbuf])

        parser = argparse.ArgumentParser()

        parser.add_argument('-d', dest='debug', action='store_true', help="runs kinto in debug mode")
        parser.add_argument('--debug', dest='debug', action='store_true', help="runs kinto in debug mode")
        parser.add_argument('-s', dest='setup', action='store_true', help="first time setup")
        parser.add_argument('--setup', dest='setup', action='store_true', help="first time setup")

        self.args = parser.parse_args()

        self.initSetup()

        global terminal
        terminal = Vte.Terminal()
        terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME']+'/.config/kinto',
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
        )
        if self.args.debug:
            if sysv:
                self.command = 'sudo /etc/init.d/kinto stop && sudo pkill -f bin/xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n'
            else:
                self.command = 'sudo systemctl stop xkeysnail && sudo pkill -f bin/xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n'
        else:
            if sysv:
                self.command = "tail -f /tmp/kinto.log\n"
            else:
                self.command = "journalctl -f --unit=xkeysnail.service -b\n"
        
        self.InputToTerm(self.command)

        grid = Gtk.Grid()
        self.add(grid)

        menubar = Gtk.MenuBar()
        grid.attach(menubar, 0, 0, 1, 1)

        scroller = Gtk.ScrolledWindow()
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(terminal)
        grid.attach(scroller, 0, 1, 1, 1)
        status_hbox = Gtk.HBox()
        status_hbox.add(self.label)
        status_hbox.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#2d303b"))
        grid.attach_next_to(status_hbox, scroller, Gtk.PositionType.BOTTOM, 2, 1)

        with open(self.kconfig) as configfile:
            autostart_line = configfile.read().split('\n')[1]

        # Autostart
        if "autostart = true" in autostart_line.casefold():
            autostart_bool = True

        if autostart_bool:
            self.menuitem_auto.set_active(True)
            self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,False)
        else:
            self.menuitem_auto.set_active(False)
            self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,True)

        menuitem_file = Gtk.MenuItem(label="File")
        menubar.append(menuitem_file)
        submenu_file = Gtk.Menu()

        menuitem_restart = Gtk.MenuItem(label="Restart")
        menuitem_restart.connect('activate',self.runRestart)
        submenu_file.append(menuitem_restart)
        menuitem_stop = Gtk.MenuItem(label="Stop")
        menuitem_stop.connect('activate',self.runStop)
        submenu_file.append(menuitem_stop)

        menuitem_file.set_submenu(submenu_file)
        submenu_file.append(self.menuitem_auto)
        kintotray = int(self.queryConfig('ps -aux | grep [k]intotray >/dev/null 2>&1 && echo "1" || echo "0"'))
        if kintotray and os.path.exists(os.environ['HOME']+'/.config/autostart/kintotray.desktop'):
            self.menuitem_systray.set_active(True)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,False)
        else:
            self.menuitem_systray.set_active(False)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,True)
        menuitem_file.connect('activate',self.refreshFile)
        submenu_file.append(self.menuitem_systray)

        menuitem_quit = Gtk.MenuItem(label="Quit")
        submenu_file.append(menuitem_quit)
        menuitem_quit.connect('activate', self.on_menu_quit)

        menuitem_edit = Gtk.MenuItem(label="Edit")
        menubar.append(menuitem_edit)
        submenu_edit = Gtk.Menu()
        menuitem_edit.set_submenu(submenu_edit)
        edititem_tweaks = Gtk.MenuItem(label="Tweaks")
        edititem_tweaks.connect('activate',self.setTweaks)
        submenu_edit.append(edititem_tweaks)
        edititem_config = Gtk.MenuItem(label="Kinto Config (shortcuts)")
        edititem_config.connect('activate',self.setConfig)
        submenu_edit.append(edititem_config)
        edititem_service = Gtk.MenuItem(label="Kinto Service")
        edititem_service.connect('activate',self.setService)
        submenu_edit.append(edititem_service)
        edititem_shortcuts = Gtk.MenuItem(label="System Shortcuts")
        edititem_shortcuts.connect('activate',self.setSysKB)
        submenu_edit.append(edititem_shortcuts)
        edititem_language = Gtk.MenuItem(label="Change Language")
        edititem_language.connect('activate',self.setRegion)
        submenu_edit.append(edititem_language)

        keyboards = Gtk.MenuItem(label="Keyboard")
        keyboards.connect('activate',self.refresh)
        menubar.append(keyboards)

        menuitem_help = Gtk.MenuItem(label="Help")
        menubar.append(menuitem_help)
        submenu_help = Gtk.Menu()
        helpitem_debug = Gtk.MenuItem(label="Debug")
        helpitem_debug.connect('activate',self.runDebug)
        submenu_help.append(helpitem_debug)
        helpitem_support = Gtk.MenuItem(label="Support")
        helpitem_support.connect('activate',self.openSupport)
        submenu_help.append(helpitem_support)
        menuitem_help.set_submenu(submenu_help)
        helpitem_about = Gtk.MenuItem(label="About")
        helpitem_about.connect('activate',self.runAbout)
        submenu_help.append(helpitem_about)

        menu = Gtk.Menu()
        keyboards.set_submenu(menu)

        self.refreshKB()

        self.mackb.signal_id = self.mackb.connect('activate',self.setKB,"mac")
        self.winkb.signal_id = self.winkb.connect('activate',self.setKB,"win")
        self.chromekb.signal_id = self.chromekb.connect('activate',self.setKB,"chrome")
        self.ibmkb.signal_id = self.ibmkb.connect('activate',self.setKB,"ibm")
        self.winmackb.signal_id = self.winmackb.connect('activate',self.setKB,"winmac")

        menu.append(self.winkb)
        menu.append(self.mackb)
        menu.append(self.chromekb)
        menu.append(self.ibmkb)
        menu.append(self.winmackb)

        GLib.timeout_add(2000, self.update_terminal)

    def setKinto(self):



        global restartsvc
        if self.options["kbtype"] == "mac":
            print("setup mac")
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
            self.mackb.disconnect(self.mackb.signal_id)
            self.mackb.set_active(True)
            self.mackb.signal_id = self.mackb.connect('activate',self.setKB,"mac")
        elif self.options["kbtype"] == "win":
            print("setup win")
            setkb = 's/^(\s{3})(\s{1}#)(.*# WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)( Default Win)|^(\s{3})(\s{1}# )(-)(- Default Mac*)/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$21$21$22$24$26/g'
            self.winkb.disconnect(self.winkb.signal_id)
            self.winkb.set_active(True)
            self.winkb.signal_id = self.winkb.connect('activate',self.setKB,"win")
        elif self.options["kbtype"] == "ibm":
            print("setup ibm")
            setkb ='s/^(\s{3})(\s{1}#)(.*# IBM.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Chromebook.*)|^(\s{3})(\s{1}# )(-)(- Default (Win|Mac.*))/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$22/g'
            self.ibmkb.disconnect(self.ibmkb.signal_id)
            self.ibmkb.set_active(True)
            self.ibmkb.signal_id = self.ibmkb.connect('activate',self.setKB,"ibm")
        elif self.options["kbtype"] == "cbk":
            print("setup chromebook")
            setkb = 's/^(\s{3})(\s{1}#)(.*# Chromebook.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(WinMac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(Mac.*)|^(?!\s{4}#)(\s{3})(\s{1})(.*)( # )(IBM.*)|^(\s{3})(\s{1}# )(-)(- Default (Win|Mac.*))/   $3$7$6$7$8$12$11$12$13$17$16$17$18$20$22/g'
            # Really an xfce4 check needs to occur before setting this 
            self.queryConfig('perl -pi -e "s/(# )(.*)(# xfce4)/\$2\$3/g" ~/.config/kinto/kinto.py')
            self.queryConfig('perl -pi -e "s/(\w.*)(# Default)/# \$1\$2/g" ~/.config/kinto/kinto.py')
            self.chromekb.disconnect(self.chromekb.signal_id)
            self.chromekb.set_active(True)
            self.chromekb.signal_id = self.chromekb.connect('activate',self.setKB,"chrome")
        elif self.options["kbtype"] == "wmk":
            print("setup winmac")
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
            self.winmackb.disconnect(self.winmackb.signal_id)
            self.winmackb.set_active(True)
            self.winmackb.signal_id = self.winmackb.connect('activate',self.setKB,"winmac")

        cmds = ['perl','-pi','-e',setkb,os.environ['HOME']+'/.config/kinto/kinto.py']
        cmdsTerm = Popen(cmds)
        cmdsTerm.wait()

        if not self.options["rightmod"]:
            if self.options["kbtype"] == "win" or self.options["kbtype"] == "wmk":
                setmod = 's/^(\s{4})((# )(.*)(# )(WinMac - Multi-language.*)|(K)(.*)(# )(WinMac - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.options["kbtype"] == "mac":
                setmod = 's/^(\s{4})((# )(.*)(# )(Mac - Multi-language.*)|(K)(.*)(# )(Mac - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.options["kbtype"] == "cbk":
                setmod = 's/^(\s{4})((# )(.*)(# )(Chromebook - Multi-language.*)|(K)(.*)(# )(Chromebook - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            if self.options["kbtype"] == "ibm":
                setmod = 's/^(\s{4})((# )(.*)(# )(IBM - Multi-language.*)|(K)(.*)(# )(IBM - Multi-language.*))/    $4$5$6$9$7$8$9$10/g'
            cmdmod = ['perl','-pi','-e',setmod,os.environ['HOME']+'/.config/kinto/kinto.py']
            cmdsTerm = Popen(cmdmod)
            cmdsTerm.wait()
        else:
            print("Right mod true - don't do a thing")

        if self.options["vsc2st3"]:
            print('Setup ST3 maps on VSCode')
            setvsc = 's/^(\s{4})(\w.*)(# )(Default - Sublime)|^(\s{4})(# )(\w.*)(# Default - Sublime)/$5$7$8$1$3$2$3$4/g'
            cmdvsc = ['perl','-pi','-e',setvsc,os.environ['HOME']+'/.config/kinto/kinto.py']
            cmdsTerm = Popen(cmdvsc)
            cmdsTerm.wait()
        if self.options["capslock"] == "esc_cmd":
            print("remap capslock to esc_cmd")
            setcaps = 's/^(\s{4})((# )(\{\w.*)(# Caps2Esc - Chrome.*)|(\{\w.*)(# )(Caps2Esc\n)|(\{.*)(# )(Caps2Esc - Chrome.*|Placeholder)|(\w.*)(# )(Caps2Cmd.*)|(# )(\{.*)(# )(Placeholder))/    $4$5$7$6$7$8$10$9$10$11$13$12$13$14$16$17$18/g'
        elif self.options["capslock"] == "cmd":
            print("remap capslock to cmd only")
            setcaps = 's/^(\s{4})((\w.*)(# )(Caps2Cmd - Chrome.*)|(\w.*)(# )(Caps2Cmd\n)|(# )(\w.*)(# )(Caps2Cmd - Chrome.*)|(\{\w.*)(# )(Caps2Esc.*)|(# )(\{.*)(# )(Placeholder))/    $4$3$4$5$7$6$7$8$10$11$12$14$13$14$15$17$18$19/g'
        if self.options["capslock"] == "esc_cmd" or self.options["capslock"] == "cmd":
            cmdcaps = ['perl','-pi','-e',setcaps,os.environ['HOME']+'/.config/kinto/kinto.py']
            cmdsTerm = Popen(cmdcaps)
            cmdsTerm.wait()

        if self.options["autostart"]:
            self.queryConfig('cp '+os.environ['HOME']+'/.config/kinto/xkeysnail.desktop '+os.environ['HOME']+'/.config/autostart/xkeysnail.desktop')
        if self.options["systray"]:
            self.queryConfig('cp '+os.environ['HOME']+'/.config/kinto/kintotray.desktop '+os.environ['HOME']+'/.config/autostart/kintotray.desktop')
            self.queryConfig("nohup python3 ~/.config/kinto/kintotray.py >/dev/null 2>&1 &")
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(True)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,False)

        restartsvc = True
    
    def initSetup(self):
        global win,openWin,restartsvc
        
        checkkb = "perl -ne 'print if /^\s+K.*# (Mac|WinMac|(Chromebook |Chromebook\n)|IBM)/' ~/.config/kinto/kinto.py | wc -l"
        checkkb_result = int(self.queryConfig(checkkb))

        if checkkb_result == 0:
            print('keyboard is not set')
            if not os.path.exists(os.environ['HOME']+'/.config/kinto/initkb'):
                Popen(['cp','/opt/kinto/initkb',os.environ['HOME']+'/.config/kinto/initkb'])

            with open(os.environ['HOME']+'/.config/kinto/initkb', 'r') as file:
                initkb_file = file.read()

            # Don't be clever - the single characters simply match the word options
            # below, makes the line shorter, but less understandable.
            tokenValue = re.findall(r'(e|d|3|k|y|t)\s=\s(\w+)', initkb_file,re.MULTILINE)

            try:
                self.options["kbtype"]    = tokenValue[0][1]
                self.options["rightmod"]  = bool(strtobool(tokenValue[1][1]))
                self.options["vsc2st3"]   = bool(strtobool(tokenValue[2][1]))
                self.options["capslock"]  = tokenValue[3][1]
                self.options["systray"]   = bool(strtobool(tokenValue[4][1]))
                self.options["autostart"] = bool(strtobool(tokenValue[5][1]))
            except IndexError:
                pass
        else:
            # If keyboard is already set and a setup argument is not being passed
            # Then load up the normal window.
            if not self.args.setup:
                openWin = True
                return

        # Set kbtype automatically
        if self.options["kbtype"] != "ask":
            openWin = True
            self.setKinto()
            # win.show_all()
        else:
            openWin = False
            restartsvc = False
            self.setupwin.set_keep_above(True);

            path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
            width = -1
            height = 128
            preserve_aspect_ratio = True

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
            self.setupwin.set_default_icon_list([pixbuf])

            self.setupwin.set_title("Keyboard Assistant")
            self.setupwin.set_size_request(600, 360)
            self.setupwin.set_resizable(False)
            self.setupwin.set_position(Gtk.WindowPosition.CENTER)

            self.setupwin.add(self.overlay)
            self.setupwin.signal_id = 0
            
            from PIL import Image

            img1 = Image.open(os.environ['HOME']+'/.config/kinto/gui/tuxbg.png')
            img2 = Image.open(os.environ['HOME']+'/.config/kinto/gui/capslock_1200x720.png')
            img3 = Image.open(os.environ['HOME']+'/.config/kinto/gui/keys_1200x720.png')

            pixbuf2 = self.image2pixbuf(Image.alpha_composite(img1, img2))
            pixbuf2 = pixbuf2.scale_simple(600, 360, GdkPixbuf.InterpType.BILINEAR)
            
            pixbuf3 = self.image2pixbuf(Image.alpha_composite(img1, img3))
            pixbuf3 = pixbuf3.scale_simple(600, 360, GdkPixbuf.InterpType.BILINEAR)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.environ['HOME']+'/.config/kinto/gui/tuxcry4.png')
            pixbuf = pixbuf.scale_simple(600, 360, GdkPixbuf.InterpType.BILINEAR)
            self.bgsuccess4 = self.bgsuccess4.new_from_pixbuf(pixbuf)
            self.bgsuccess4.set_valign(Gtk.Align.END)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.environ['HOME']+'/.config/kinto/gui/tuxuninstall.png')
            pixbuf = pixbuf.scale_simple(600, 360, GdkPixbuf.InterpType.BILINEAR)
            self.bguninstall = self.bguninstall.new_from_pixbuf(pixbuf)
            self.bguninstall.set_valign(Gtk.Align.END)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.environ['HOME']+'/.config/kinto/gui/tuxbg.png')
            pixbuf = pixbuf.scale_simple(600, 360, GdkPixbuf.InterpType.BILINEAR)
            self.background = self.background.new_from_pixbuf(pixbuf)
            self.background.set_valign(Gtk.Align.END)
            self.bgcaps = self.bgcaps.new_from_pixbuf(pixbuf2)
            self.bgspace = self.bgspace.new_from_pixbuf(pixbuf3)
            self.bgspace.set_valign(Gtk.Align.END)
            self.overlay.add(self.background)
            self.overlay.add_overlay(self.container)
            self.setupwin.add(self.container)

            self.main = Main(self)
            self.container.add(self.main)
            self.uninstall_page = UninstallPage(self)
            self.first_page = FirstPage(self)
            self.container.add(self.first_page)
            self.second_page = SecondPage(self)
            self.caps_page = CapsPage(self)
            self.success_page = SuccessPage(self)

            self.setupwin.show_all()
            self.setupwin.connect('delete-event', self.on_delete_event)

            return

    def image2pixbuf(self,im):
        data = im.tobytes()
        w, h = im.size
        # print(im.size)
        data = GLib.Bytes.new(data)
        pix = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,True, 8, w, h, w * 4)
        return pix

    def refreshFile(self,button):
        kintotray = int(self.queryConfig('ps -aux | grep [k]intotray >/dev/null 2>&1 && echo "1" || echo "0"'))
        if os.path.exists(os.environ['HOME']+'/.config/autostart/kintotray.desktop') and kintotray and self.menuitem_systray.get_active() == False:
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(True)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,False)
        elif os.path.exists(os.environ['HOME']+'/.config/autostart/kintotray.desktop') and not kintotray and self.menuitem_systray.get_active() == True:
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(False)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,True)
        elif not os.path.exists(os.environ['HOME']+'/.config/autostart/kintotray.desktop') and self.menuitem_systray.get_active() == True:
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(False)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,True)
        # return

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
            self.ibmkb.set_active(True)
            countkb += 1

        if countkb > 1:
            Popen(['notify-send','Kinto: Remove ' + str(countkb-1) + ' kb type(s)'])

        return

    def runDebug(self,button):
        if sysv:
            command = 'send \003 sudo /etc/init.d/kinto stop && sudo pkill -f bin/xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n'
        else:
            command = 'send \003 sudo systemctl stop xkeysnail && sudo pkill -f bin/xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n'
        self.InputToTerm(command)

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

        # Checking if the user is using a light or dark theme
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

    def checkTray(self,button,tray_bool):
        kintotray = int(self.queryConfig('ps -aux | grep [k]intotray >/dev/null 2>&1 && echo "1" || echo "0"'))
        if tray_bool:
            Popen(['cp',os.environ['HOME']+'/.config/kinto/kintotray.desktop',os.environ['HOME']+'/.config/autostart/kintotray.desktop'])
            if not kintotray:
                Popen([os.environ['HOME']+'/.config/kinto/kintotray.py'])
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(True)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,False)
        else:
            Popen(['rm',os.environ['HOME']+'/.config/autostart/kintotray.desktop'])
            Popen(['pkill','-f','kintotray.py'])
            killspawn = "for pid in `ps -ef | grep 'active xkeysnail' | awk '{print $2}'` ; do kill -2 $pid ; done"
            self.queryConfig(killspawn)
            time.sleep(1)
            global child_pid
            if sysv:
                self.kinto_status = Popen("export TERM=xterm-color;while :; do clear; pgrep 'xkeysnail'; sleep 2; done", stdout=PIPE, shell=True)
            else:
                self.kinto_status = Popen("export TERM=xterm-color;while :; do clear; systemctl is-active xkeysnail; sleep 2; done", stdout=PIPE, shell=True)
            child_pid = self.kinto_status.pid
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(False)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,True)
        return

    def setKB(self,button,kbtype):
        global sysv
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

            if sysv:
                restart = ['sudo', '-E','/etc/init.d/kinto','restart']
            else:
                restart = ['sudo', 'systemctl','restart','xkeysnail']
            cmds = ['perl','-pi','-e',setkb,self.kconfig]

            cmdsTerm = Popen(cmds)
            cmdsTerm.wait()

            Popen(restart)

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error Resetting KB Type!'])

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
        global restartsvc, openWin, sysv
        
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
        if openWin and self.get_title() == "Keyboard Assistant":
            openWin = False
            win.show_all()
        elif self.get_title() == "Keyboard Assistant":
             Gtk.main_quit()

        self.hide()
        self.destroy()

        return True

    def queryConfig(self,query):
        res = Popen(query, stdout=PIPE, stderr=None, shell=True)
        res.wait()
        return res.communicate()[0].strip().decode('UTF-8')

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
                pkillxkey = Popen(['sudo', 'pkill','-f','bin/xkeysnail'])
                pkillxkey.wait()
            if sysv:
                Popen(['sudo','-E','/etc/init.d/kinto','start'])
                self.command = "send \003 tail -f /tmp/kinto.log\n"
            else:
                Popen(['sudo','systemctl','start','xkeysnail'])
                self.command = "send \003 journalctl -f --unit=xkeysnail.service -b\n"
            self.InputToTerm(self.command)
        except:
            Popen(['notify-send','Kinto: Errror restarting Kinto!'])

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

    def setAutostart(self,button,autostart):
        try:
            if autostart == False:
                Popen(['perl','-pi','-e','s/autostart = true/autostart = false/g',os.environ['HOME']+'/.config/kinto/kinto.py'])
                self.menuitem_auto.set_active(False)
                self.menuitem_auto.disconnect(self.menuitem_auto.signal_id)
                self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,True)
            else:
                Popen(['perl','-pi','-e','s/autostart = false/autostart = true/g',os.environ['HOME']+'/.config/kinto/kinto.py'])
                self.menuitem_auto.set_active(True)
                self.menuitem_auto.disconnect(self.menuitem_auto.signal_id)
                self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,False)

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

    def remove_control_characters(self,s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

    def non_block_read(self):
        ''' even in a thread, a normal read with block until the buffer is full '''
        output = self.kinto_status.stdout
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        op = output.read()
        if op == None:
            return ''

        status = op.decode('utf-8').rstrip()
        if "inactive" in status:
            if "journalctl" in self.command:
                stats = "<span color='red'><b>inactive</b></span>"
            else:
                stats = "<span color='yellow'><b>Debug Mode</b></span>"
        elif "active" in status:
            stats = "<span color='#66ff00'><b>active</b></span>"
        else:
            # "failed" in status or "deactivating" in status or "activating" in status
            if "journalctl" in self.command:
                stats = "<span color='red'><b>inactive</b></span>"
            else:
                stats = "<span color='yellow'><b>Debug Mode</b></span>"

        return stats

    def remove_tags(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html).strip()
        return cleantext

    def update_terminal(self):
        status = self.non_block_read()
        if self.label.get_text().strip() != self.remove_tags(status):
            self.label.set_markup("  " + status + "  ")
        return self.kinto_status.poll() is None

    def key_press_event(self, widget, event):
        global openWin
        trigger = "None"
        keyname = Gdk.keyval_name(event.keyval)
        current = self.second_page
        bg = self.bgsuccess4
        onward = self.success_page
        print("page value: "+str(self.page))

        if self.page == 1 and "Control" in keyname and openWin == False:
            print("IBM or Chromebook")
            print("Continue to page 2")
            bg = self.bgcaps
            onward = self.caps_page
            trigger = "Half"
            self.page += 1
        elif self.page == 2 and "Caps_Lock" in keyname and event.state & Gdk.ModifierType.LOCK_MASK:
            print("Set IBM Keyboard")
            current = self.caps_page
            self.options["kbtype"] = "ibm"
            trigger = "Done"
        elif self.page == 2 and "Super" in keyname:
            print("Set Chromebook Keyboard")
            current = self.caps_page
            self.options["kbtype"] = "cbk"
            trigger = "Done"
        elif self.page == 1 and "Alt" in keyname:
            print("Set Mac Keyboard")
            self.options["kbtype"] = "mac"
            trigger = "Done"
        elif self.page == 1 and "Super" in keyname:
            print("Set Win Keyboard")
            self.options["kbtype"] = "win"
            trigger = "Done"

        if trigger == "Half" or trigger == "Done" and openWin == False:
            for grandkid in self.overlay.get_children():
                self.overlay.remove(grandkid)
            self.overlay.add(bg)
            self.overlay.add_overlay(self.container)
            self.container.add(onward)
            self.container.remove(current)
            # self.setupwin.disconnect(self.setupwin.signal_id)
        if trigger == "Half" and openWin == False:
            # print("reset key_press_event")
            # self.setupwin.signal_id = self.setupwin.connect("key_press_event", self.key_press_event)
            self.setupwin.show_all()
        elif trigger == "Done" and openWin == False:
            print("in Done")
            self.setKinto()
            self.setupwin.show_all()
            openWin = True
            self.last_onward.grab_focus()
            # print(self.setupwin.signal_id)
            self.setupwin.disconnect(self.setupwin.signal_id)
            # print(self.setupwin.signal_id)
        print("key press event is on")

    def InputToTerm(self,cmd):
        # Not clearly known which VTE versions
        # requires which fix
        try:
            query = str.encode(cmd)
            terminal.feed_child_binary(query)
        except:
            pass
            try:
                terminal.feed_child(cmd,len(cmd))
            except:
                pass

        # print(Vte.get_minor_version())

    # def on_menu_auto(self, widget):
    #     print("add file open dialog")

    # def on_menu_enable(self, widget):
    #     print("add file open dialog")

    def on_menu_quit(self, widget):
        Gtk.main_quit()

class Main(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window

class UninstallPage(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window

        self.grid = Gtk.Grid()
        vbox = Gtk.VBox()
        vbox_container = Gtk.VBox()
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        label_start = Gtk.Label()
        label_start.set_markup('<b>Uninstall</b>\n\n\n\nWould you like to uninstall kinto?\n\n If you need support please visit <a href="http://kinto.sh">kinto.sh</a>.')
        label_start.set_valign(Gtk.Align.START)
        label_start.set_halign(Gtk.Align.START)

        label_start.set_line_wrap(True)
        vbox.add(label_start)
        scroller.add(vbox)

        hbox = Gtk.HBox()
        previous = Gtk.Button(label="Uninstall")
        previous.connect("clicked", self.goback)
        previous.set_margin_end(206)
        hbox.add(previous)

        onward = Gtk.Button(label="Continue")
        onward.connect("clicked", self.forward)
        hbox.add(onward)

        hbox.set_hexpand(False)
        hbox.set_vexpand(False)
        hbox.set_margin_bottom(6)
        hbox.set_margin_end(25)

        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        vbox_container.add(scroller)
        vbox_container.set_margin_top(55)
        vbox_container.set_margin_end(25)
        self.grid.set_margin_start(157)
        vbox_container.set_margin_bottom(18)
        vbox.set_margin_end(10)
        vbox.set_margin_bottom(18)
        self.grid.add(vbox_container)
        self.grid.attach_next_to(hbox, vbox_container, Gtk.PositionType.BOTTOM, 2, 1)
        self.add(self.grid)

    def goback(self, *args):
        self.hide()

    def forward(self, *args):
        for grandkid in self.__parent_window.overlay.get_children():
            self.__parent_window.overlay.remove(grandkid)
        self.__parent_window.overlay.add(self.__parent_window.background)
        self.__parent_window.overlay.add_overlay(self.__parent_window.container)
        self.__parent_window.container.add(self.__parent_window.first_page)
        self.__parent_window.container.remove(self.__parent_window.uninstall_page)
        self.__parent_window.setupwin.show_all()
        self.hide()

class FirstPage(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window

        self.grid = Gtk.Grid()
        vbox = Gtk.VBox()
        vbox_container = Gtk.VBox()
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        label_start = Gtk.Label()
        label_start.set_markup("Before we continue please make sure you do not have any other remappers running. Kinto works best when it is the only application remapping your keys.\n\nBy continuing you also agree that Kinto is not held liable for any harm, damage(s) or unexpected behaviors.\nThis software is free, open-source, and provided as-is.\n\n<sup><b>© 2019, 2020 by Ben Reaves ~ Kinto is licensed on GPLv2.</b></sup>")
        label_start.set_valign(Gtk.Align.START)
        label_start.set_halign(Gtk.Align.START)
        label_start.set_line_wrap(True)
        vbox.add(label_start)
        scroller.add(vbox)

        hbox = Gtk.HBox()
        previous = Gtk.Button(label="")
        for child in previous.get_children():
            child.set_label("<b>Decline</b>")
            child.set_use_markup(True)
        previous.connect("clicked", self.goback)
        previous.set_margin_end(245)
        hbox.add(previous)

        self.__parent_window.first_onward.set_label("")
        for child in self.__parent_window.first_onward.get_children():
            child.set_label("<b>Agree</b>")
            child.set_use_markup(True)
        self.__parent_window.first_onward.set_active(True)
        self.__parent_window.first_onward.connect("clicked", self.forward)

        hbox.add(self.__parent_window.first_onward)
        hbox.set_hexpand(False)
        hbox.set_vexpand(False)
        hbox.set_margin_bottom(6)
        hbox.set_margin_end(25)

        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        vbox_container.add(scroller)
        vbox_container.set_margin_top(55)
        vbox_container.set_margin_end(28)
        self.grid.set_margin_start(157)
        vbox_container.set_margin_bottom(18)
        vbox.set_margin_end(10)
        vbox.set_margin_bottom(18)
        self.grid.add(vbox_container)
        self.grid.attach_next_to(hbox, vbox_container, Gtk.PositionType.BOTTOM, 2, 1)
        self.add(self.grid)
        self.__parent_window.first_onward.grab_focus()

    def goback(self, *args):
        Gtk.main_quit()
        self.hide()

    def forward(self, button):
        self.__parent_window.first_onward.set_active(True)
        for grandkid in self.__parent_window.overlay.get_children():
            self.__parent_window.overlay.remove(grandkid)
        self.__parent_window.overlay.add(self.__parent_window.bgspace)
        self.__parent_window.overlay.add_overlay(self.__parent_window.container)
        self.__parent_window.container.add(self.__parent_window.second_page)
        # print(self.__parent_window.setupwin.signal_id)
        self.__parent_window.setupwin.signal_id = self.__parent_window.setupwin.connect("key_press_event", self.__parent_window.key_press_event)
        # print(self.__parent_window.setupwin.signal_id)
        self.__parent_window.container.remove(self.__parent_window.first_page)
        self.__parent_window.setupwin.show_all()
        self.hide()

class SecondPage(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window

        self.grid = Gtk.Grid()
        vbox = Gtk.VBox()
        vbox_container = Gtk.VBox()
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        label_start = Gtk.Label()
        
        label_start.set_markup('<b>Identifying your Keyboard...</b>\n\nPress the <b>2nd</b> key <b>Left</b> of the spacebar.\n\n<sub>If stuck here then unset Overlay (Super) key on your DE.</sub>')
        label_start.set_valign(Gtk.Align.START)
        label_start.set_halign(Gtk.Align.START)
        label_start.set_line_wrap(True)
        vbox.add(label_start)
        scroller.add(vbox)

        hbox = Gtk.HBox()
        previous = Gtk.Button(label="")
        for child in previous.get_children():
            child.set_label("<b>Go Back</b>")
            child.set_use_markup(True)
        previous.connect("clicked", self.goback)
        previous.set_margin_end(315)
        hbox.add(previous)

        # onward = Gtk.Button(label="Continue")
        # onward.connect("clicked", self.forward)
        # hbox.add(onward)

        hbox.set_hexpand(False)
        hbox.set_vexpand(False)
        hbox.set_margin_bottom(6)
        hbox.set_margin_end(25)

        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        vbox_container.add(scroller)
        vbox_container.set_margin_top(55)
        vbox_container.set_margin_end(25)
        self.grid.set_margin_start(157)
        vbox_container.set_margin_bottom(18)
        vbox.set_margin_end(10)
        vbox.set_margin_bottom(18)
        self.grid.add(vbox_container)
        self.grid.attach_next_to(hbox, vbox_container, Gtk.PositionType.BOTTOM, 2, 1)
        self.add(self.grid)

    def goback(self, *args):
        for grandkid in self.__parent_window.overlay.get_children():
            self.__parent_window.overlay.remove(grandkid)
        self.__parent_window.overlay.add(self.__parent_window.background)
        self.__parent_window.overlay.add_overlay(self.__parent_window.container)
        self.__parent_window.container.add(self.__parent_window.first_page)
        self.__parent_window.container.remove(self.__parent_window.second_page)
        self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)
        self.__parent_window.setupwin.show_all()
        self.__parent_window.first_onward.grab_focus()
        self.hide()

    # def capsforward(self, *args):
    #     for grandkid in self.__parent_window.overlay.get_children():
    #         self.__parent_window.overlay.remove(grandkid)
    #     self.__parent_window.overlay.add(self.__parent_window.bgcaps)
    #     self.__parent_window.overlay.add_overlay(self.__parent_window.container)
    #     self.__parent_window.container.add(self.__parent_window.caps_page)
    #     self.__parent_window.container.remove(self.__parent_window.second_page)
    #     self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)
    #     self.__parent_window.setupwin.signal_id = self.__parent_window.setupwin.connect("key_press_event", self.__parent_window.key_press_event,2)
    #     self.__parent_window.setupwin.show_all()
    #     self.hide()

    # def forward(self, *args):
    #     for grandkid in self.__parent_window.overlay.get_children():
    #         self.__parent_window.overlay.remove(grandkid)
    #     self.__parent_window.overlay.add(self.__parent_window.bgsuccess4)
    #     self.__parent_window.overlay.add_overlay(self.__parent_window.container)
    #     self.__parent_window.container.add(self.__parent_window.success_page)
    #     self.__parent_window.container.remove(self.__parent_window.second_page)
    #     self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)
    #     self.__parent_window.setupwin.show_all()
    #     self.hide()

class CapsPage(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window

        self.grid = Gtk.Grid()
        vbox = Gtk.VBox()
        vbox_container = Gtk.VBox()
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        label_start = Gtk.Label()
        label_start.set_markup('<b>Identifying your Keyboard...</b>\n\nPress the <b>capslock</b> key twice.')
        label_start.set_valign(Gtk.Align.START)
        label_start.set_halign(Gtk.Align.START)
        label_start.set_line_wrap(True)
        vbox.add(label_start)
        scroller.add(vbox)

        hbox = Gtk.HBox()
        previous = Gtk.Button(label="")
        for child in previous.get_children():
            child.set_label("<b>Go Back</b>")
            child.set_use_markup(True)
        previous.connect("clicked", self.goback)
        previous.set_margin_end(315)
        hbox.add(previous)

        # onward = Gtk.Button(label="Continue")
        # onward.connect("clicked", self.forward)
        # hbox.add(onward)

        hbox.set_hexpand(False)
        hbox.set_vexpand(False)
        hbox.set_margin_bottom(6)
        hbox.set_margin_end(25)

        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        vbox_container.add(scroller)
        vbox_container.set_margin_top(55)
        vbox_container.set_margin_end(25)
        self.grid.set_margin_start(157)
        vbox_container.set_margin_bottom(18)
        vbox.set_margin_end(10)
        vbox.set_margin_bottom(18)
        self.grid.add(vbox_container)
        self.grid.attach_next_to(hbox, vbox_container, Gtk.PositionType.BOTTOM, 2, 1)
        self.add(self.grid)

    def goback(self, *args):
        for grandkid in self.__parent_window.overlay.get_children():
            self.__parent_window.overlay.remove(grandkid)
        self.__parent_window.overlay.add(self.__parent_window.bgspace)
        self.__parent_window.overlay.add_overlay(self.__parent_window.container)
        self.__parent_window.container.add(self.__parent_window.second_page)
        self.__parent_window.page = 1
        # self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)
        # self.__parent_window.setupwin.signal_id = self.__parent_window.setupwin.connect("key_press_event", self.__parent_window.key_press_event)
        self.__parent_window.container.remove(self.__parent_window.caps_page)
        self.__parent_window.setupwin.show_all()
        self.hide()

    # def forward(self, *args):
    #     for grandkid in self.__parent_window.overlay.get_children():
    #         self.__parent_window.overlay.remove(grandkid)
    #     self.__parent_window.overlay.add(self.__parent_window.bgsuccess4)
    #     self.__parent_window.overlay.add_overlay(self.__parent_window.container)
    #     self.__parent_window.container.add(self.__parent_window.success_page)
    #     self.__parent_window.container.remove(self.__parent_window.caps_page)
    #     self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)
    #     self.__parent_window.setupwin.show_all()
    #     self.hide()

class SuccessPage(Gtk.Box):
    def __init__(self, parent_window):
        super().__init__(spacing=10)
        self.__parent_window = parent_window
        self.grid = Gtk.Grid()

        hbox = Gtk.HBox()
        previous = Gtk.Button(label="       ")
        previous.props.relief = Gtk.ReliefStyle.NONE
        previous.set_margin_end(245)
        hbox.add(previous)

        self.__parent_window.last_onward.set_label("")
        for child in self.__parent_window.last_onward.get_children():
            child.set_label("<b>Done</b>")
            child.set_use_markup(True)
        self.__parent_window.last_onward.connect("clicked", self.forward)

        hbox.add(self.__parent_window.last_onward)
        hbox.set_hexpand(False)
        hbox.set_vexpand(False)
        hbox.set_margin_bottom(6)
        hbox.set_margin_end(25)

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        vbox = Gtk.VBox()
        vbox_container = Gtk.VBox()
        vbox_container.set_margin_top(55)
        vbox_container.set_margin_end(28)
        vbox_container.add(scroller)
        self.grid.set_margin_start(157)
        vbox_container.set_margin_bottom(18)
        vbox.set_margin_end(10)
        vbox.set_margin_bottom(18)
        self.grid.add(vbox_container)
        self.grid.attach_next_to(hbox, vbox_container, Gtk.PositionType.BOTTOM, 2, 1)
        self.add(self.grid)
        self.__parent_window.last_onward.grab_focus()

    def forward(self, *args):
        self.hide()
        # self.__parent_window.setupwin.disconnect(self.__parent_window.setupwin.signal_id)/
        self.__parent_window.setupwin.close()


global win,openWin
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
if openWin:
    win.show_all()
    openWin = False

Gtk.main()
