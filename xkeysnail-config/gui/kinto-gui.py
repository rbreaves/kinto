#!/usr/bin/env python3

import gi,os,time,fcntl,argparse,re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GdkPixbuf
from gi.repository import Vte,GLib
from subprocess import Popen,PIPE,CalledProcessError

import signal

def kill_child():
    if child_pid is None:
        pass
    else:
        os.kill(child_pid, signal.SIGTERM)

import atexit
atexit.register(kill_child)

class MyWindow(Gtk.Window):

    label = Gtk.Label()
    label.set_alignment(1, 0)
    ostype = os.environ.get('XDG_CURRENT_DESKTOP')

    global child_pid
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

    menuitem_enable = Gtk.CheckMenuItem(label="Enabled")
    menuitem_enable.signal_id = 0
    menuitem_auto = Gtk.CheckMenuItem(label="Autostart")
    menuitem_auto.signal_id = 0
    menuitem_systray = Gtk.CheckMenuItem(label="Tray Enabled")
    menuitem_systray.signal_id = 0

    def __init__(self):

        Gtk.Window.__init__(self, title="Kinto.sh")
        # self.set_icon_from_file(os.environ['HOME']+'/.config/kinto/kinto-color.svg')
        # self.set_gravity(Gdk.Gravity.NORTH_WEST)
        self.set_size_request(600, 360)

        global restartsvc 
        restartsvc = False

        homedir = os.path.expanduser("~")
        self.kconfig = homedir+"/.config/kinto/kinto.py"

        path = os.environ['HOME']+'/.config/kinto/kinto-color.svg'
        width = 256
        height = 256
        preserve_aspect_ratio = True

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, width, height, preserve_aspect_ratio)
        # image = Gtk.Image()
        # image.set_from_pixbuf(pixbuf)
        self.set_default_icon_list([pixbuf])

        # self.button = Gtk.Button("Do The Command")
        # self.button2 = Gtk.Button("End Command")
        # self.InputToTerm(self.cmdbytes)
        # self.command2 = "send \003; echo 'hello'\n"
        # # expect -c "send \003;"
        # self.cmdbytes2 = str.encode(self.command2)
        # self.button.connect("clicked", self.InputToTerm, self.cmdbytes)
        # self.button2.connect("clicked", self.InputToTerm, self.cmdbytes2)

        parser = argparse.ArgumentParser()

        # parser.add_argument('-b', type=int, required=False, help="")
        # parser.add_argument('-e', type=int, default=2, help="")
        parser.add_argument('-d', dest='debug', action='store_true', help="runs kinto in debug mode")
        parser.add_argument('--debug', dest='debug', action='store_true', help="runs kinto in debug mode")

        args = parser.parse_args()

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

        if args.debug:
            # print("run debug")
            self.command = "sudo systemctl stop xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n"
        else:
            self.command = "journalctl -f --unit=xkeysnail.service -b\n"
        
        self.cmdbytes = str.encode(self.command)
        self.InputToTerm(self.cmdbytes)

        grid = Gtk.Grid()
        grid.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("#2d303b"))
        self.add(grid)

        menubar = Gtk.MenuBar()
        # menubar.set_hexpand(True)
        grid.attach(menubar, 0, 0, 1, 1)
        # grid.add(menubar)

        # grid.add(self.button)
        # grid.add(self.button2)
        # grid.add(self.status)
        # grid.attach(self.button, 0, 1, 1, 1)
        # grid.attach(self.button2, 1, 1, 1, 1)

        scroller = Gtk.ScrolledWindow()
        # scroller.set_size_request(200,100)
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(terminal)
        grid.attach(scroller, 0, 1, 1, 1)
        # grid.add(scroller)
        # grid.attach(scroller, 0, 0, 2, 2)
        grid.attach_next_to(self.label, scroller, Gtk.PositionType.BOTTOM, 2, 1)
        # grid.attach_next_to(self.label2, self.label, Gtk.PositionType.RIGHT, 2, 1)

        # three labels
        label_top_left = Gtk.Label(label="Top left")
        another = Gtk.Label(label="another")
        # label_top_right = Gtk.Label(label="This is Top Right")
        # label_bottom = Gtk.Label(label="This is Bottom")

        # some space between the columns of the grid
        # grid.set_column_spacing(20)

        # in the grid:
        # attach the first label in the top left corner
        # grid.add(label_top_left)
        # grid.attach(label_top_left, 0, 0, 1, 1)
        # attach the second label
        # grid.attach(label_top_right, 1, 0, 1, 1)
        # attach the third label below the first label
        # grid.attach_next_to(label_bottom, label_top_left, Gtk.PositionType.BOTTOM, 2, 1)
        # grid.attach_next_to(menubar, label_top_left, Gtk.PositionType.BOTTOM, 2, 1)

        # sw = Gtk.ScrolledWindow()
        # self.label.set_alignment(0, 0)
        # self.label.set_selectable(True)
        # self.label.set_line_wrap(True)
        # self.label.set_max_width_chars(150)
        # # sw.set_size_request(400,300)
        # sw.set_hexpand(True)
        # sw.set_vexpand(True)
        # sw.add_with_viewport(self.label)
        # # self.add(sw)
        # # grid.add(sw)
        # # grid.add(self.status)
        # grid.attach(sw, 0, 0, 2, 2)
        # # sub_proc = Popen("journalctl -f --unit=xkeysnail.service -b", stdout=PIPE, shell=True)
        # # sub_outp = ""

        with open(self.kconfig) as configfile:
            autostart_line = configfile.read().split('\n')[1]

        # Autostart
        if "autostart = true" in autostart_line.casefold():
            autostart_bool = True

        if autostart_bool:
            # Popen(['sudo', 'systemctl','restart','xkeysnail'])
            self.menuitem_auto.set_active(True)
            self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,False)
        else:
            self.menuitem_auto.set_active(False)
            self.menuitem_auto.signal_id = self.menuitem_auto.connect('activate',self.setAutostart,True)

        menuitem_file = Gtk.MenuItem(label="File")
        menubar.append(menuitem_file)
        submenu_file = Gtk.Menu()
        menuitem_file.set_submenu(submenu_file)
        submenu_file.append(self.menuitem_enable)
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
        # self.menuitem_enable.connect('activate', self.setEnable)
        menuitem_restart = Gtk.MenuItem(label="Restart")
        menuitem_restart.connect('activate',self.runRestart)
        submenu_file.append(menuitem_restart)

        menuitem_quit = Gtk.MenuItem(label="Quit")
        submenu_file.append(menuitem_quit)
        menuitem_quit.connect('activate', self.on_menu_quit)

        menuitem_edit = Gtk.MenuItem(label="Edit")
        menubar.append(menuitem_edit)
        submenu_edit = Gtk.Menu()
        menuitem_edit.set_submenu(submenu_edit)
        edititem_tweaks = Gtk.MenuItem("Tweaks")
        edititem_tweaks.connect('activate',self.setTweaks)
        submenu_edit.append(edititem_tweaks)
        edititem_config = Gtk.MenuItem("Kinto Config (shortcuts)")
        edititem_config.connect('activate',self.setConfig)
        submenu_edit.append(edititem_config)
        edititem_service = Gtk.MenuItem("Kinto Service")
        edititem_service.connect('activate',self.setService)
        submenu_edit.append(edititem_service)
        edititem_shortcuts = Gtk.MenuItem("System Shortcuts")
        edititem_shortcuts.connect('activate',self.setSysKB)
        submenu_edit.append(edititem_shortcuts)
        edititem_language = Gtk.MenuItem("Change Language")
        edititem_language.connect('activate',self.setRegion)
        submenu_edit.append(edititem_language)

        keyboards = Gtk.MenuItem(label="Keyboard")
        keyboards.connect('activate',self.refresh)
        menubar.append(keyboards)

        # tweaks = Gtk.MenuItem(label="Tweaks")
        # menubar.append(tweaks)
        # submenu_tweaks = Gtk.Menu()
        # tweaks.set_submenu(submenu_tweaks)
        # tweakitem_rightmod = Gtk.CheckMenuItem("AltGr on Right Cmd")
        # submenu_tweaks.append(tweakitem_rightmod)
        # tweakitem_vsc2st3 = Gtk.CheckMenuItem("ST3 hotkeys for VS Code")
        # submenu_tweaks.append(tweakitem_vsc2st3)
        # tweakitem_caps2esc = Gtk.CheckMenuItem("Capslock is Escape when tapped, Cmd when held")
        # submenu_tweaks.append(tweakitem_caps2esc)
        # tweakitem_caps2cmd = Gtk.CheckMenuItem("Capslock is Cmd")
        # submenu_tweaks.append(tweakitem_caps2cmd)

        menuitem_help = Gtk.MenuItem(label="Help")
        menubar.append(menuitem_help)
        submenu_help = Gtk.Menu()
        helpitem_debug = Gtk.MenuItem(label="Debug")
        helpitem_debug.connect('activate',self.runDebug)
        submenu_help.append(helpitem_debug)
        helpitem_support = Gtk.MenuItem("Support")
        helpitem_support.connect('activate',self.openSupport)
        submenu_help.append(helpitem_support)
        menuitem_help.set_submenu(submenu_help)
        helpitem_about = Gtk.MenuItem("About")
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

        # grid.add(another)

        GLib.timeout_add(2000, self.update_terminal)

        # self.show_all()

        # radiomenuitem1 = Gtk.RadioMenuItem(label="Windows")
        # radiomenuitem1.set_active(True)
        # menu.append(radiomenuitem1)
        # radiomenuitem2 = Gtk.RadioMenuItem(label="Apple", group=radiomenuitem1)
        # menu.append(radiomenuitem2)
    
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
            ibmkb.set_active(True)
            countkb += 1

        if countkb > 1:
            Popen(['notify-send','Kinto: Remove ' + str(countkb-1) + ' kb type(s)','-i','budgie-desktop-symbolic'])

        return

    def runDebug(self,button):
        # self.InputToTerm(self.cmdbytes)
        # self.command2 = "send \003; echo 'hello'\n"
        command = "send \003 sudo systemctl stop xkeysnail && sudo xkeysnail ~/.config/kinto/kinto.py\n"
        cmdbytes = str.encode(command)
        self.InputToTerm(cmdbytes)

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
        copy = Gtk.Label("Copyrighted 2019, 2020 - GPLv2")
        url = Gtk.LinkButton("http://kinto.sh", label="http://kinto.sh")
        url2 = Gtk.Label("http://kinto.sh")

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
        # path.exists('.config/autostart/kintotray.py')
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
            self.kinto_status = Popen("while :; do clear; systemctl is-active xkeysnail; sleep 2; done", stdout=PIPE, shell=True)
            child_pid = self.kinto_status.pid
            # Popen(['pkill','-f','kintotray.py'])
            self.menuitem_systray.disconnect(self.menuitem_systray.signal_id)
            self.menuitem_systray.set_active(False)
            self.menuitem_systray.signal_id = self.menuitem_systray.connect('activate',self.checkTray,True)
        return

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

            cmdsTerm = Popen(cmds)
            cmdsTerm.wait()

            Popen(restart)

        except CalledProcessError:
            Popen(['notify-send','Kinto: Error Resetting KB Type!','-i','budgie-desktop-symbolic'])

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
        global restartsvc 
        if restartsvc == True:
            try:
                restartcmd = ['sudo', 'systemctl','restart','xkeysnail']
                Popen(restartcmd)
                restartsvc = False

            except CalledProcessError:
                Popen(['notify-send','Kinto: Error restarting Kinto after setting tweaks!','-i','budgie-desktop-symbolic'])

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
            Popen(['notify-send','Kinto: Error Resetting AltGr!','-i','budgie-desktop-symbolic'])

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
            Popen(['notify-send','Kinto: Error Resetting SublimeText remaps for VSCode!','-i','budgie-desktop-symbolic'])
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
            Popen(['notify-send','Kinto: Error resetting caps2esc!','-i','budgie-desktop-symbolic'])

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
            Popen(['notify-send','Kinto: Error resetting caps2cmd!','-i','budgie-desktop-symbolic'])

        return

    def runRestart(self,button):
        try:
            stop = Popen(['sudo', 'systemctl','stop','xkeysnail'])
            stop.wait()
            time.sleep(1)
            res = Popen(['pgrep','xkeysnail'])
            res.wait()

            if res.returncode == 0:
                pkillxkey = Popen(['sudo', 'pkill','-f','bin/xkeysnail'])
                pkillxkey.wait()
            Popen(['sudo', 'systemctl','start','xkeysnail'])
            self.command = "send \003 journalctl -f --unit=xkeysnail.service -b\n"
            self.cmdbytes = str.encode(self.command)
            self.InputToTerm(self.cmdbytes)
        except:
            Popen(['notify-send','Kinto: Errror restarting Kinto!','-i','budgie-desktop-symbolic'])

    def setEnable(self,button,enableKinto):
        try:
            if enableKinto:
                res = Popen(['pgrep','xkeysnail'])
                res.wait()
                print(res.returncode)

                if res.returncode == 0:
                    # Popen(['notify-send','Kinto: Err in debug mode?','-i','budgie-desktop-symbolic'])
                    pkillxkey = Popen(['sudo', 'pkill','-f','bin/xkeysnail'])
                    pkillxkey.wait()

                Popen(['sudo', 'systemctl','restart','xkeysnail'])
                self.menuitem_enable.disconnect(self.menuitem_enable.signal_id)
                self.menuitem_enable.set_active(True)
                self.menuitem_enable.signal_id = self.menuitem_enable.connect('activate',self.setEnable,False)
                self.command = "send \003 journalctl -f --unit=xkeysnail.service -b\n"
                self.cmdbytes = str.encode(self.command)
                self.InputToTerm(cmdbytes)
            else:
                Popen(['sudo', 'systemctl','stop','xkeysnail'])
                self.command = "send \003 journalctl -f --unit=xkeysnail.service -b\n"
                self.cmdbytes = str.encode(self.command)
                self.menuitem_enable.disconnect(self.menuitem_enable.signal_id)
                self.menuitem_enable.set_active(False)
                self.menuitem_enable.signal_id = self.menuitem_enable.connect('activate',self.setEnable,True)
        except CalledProcessError:
            Popen(['notify-send','Kinto: Error enabling!','-i','budgie-desktop-symbolic'])

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
            Popen(['notify-send','Kinto: Error setting autostart!','-i','budgie-desktop-symbolic'])

    def setConfig(self,button):
        try:
            if os.path.exists('/opt/sublime_text/sublime_text'):
                Popen(['/opt/sublime_text/sublime_text',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which(gedit) is not None:
                Popen(['gedit',os.environ['HOME']+'/.config/kinto/kinto.py'])
            elif which(mousepad) is not None:
                Popen(['mousepad',os.environ['HOME']+'/.config/kinto/kinto.py'])

        except CalledProcessError:                                  # Notify user about error on running restart commands.
            Popen(['notify-send','Kinto: Error could not open config file!','-i','budgie-desktop-symbolic'])

    def setService(self,button):
        try:
            if os.path.exists('/opt/sublime_text/sublime_text'):
                Popen(['/opt/sublime_text/sublime_text','/lib/systemd/system/xkeysnail.service'])
            elif which(gedit) is not None:
                Popen(['gedit','/lib/systemd/system/xkeysnail.service'])
            elif which(mousepad) is not None:
                Popen(['mousepad','/lib/systemd/system/xkeysnail.service'])

        except CalledProcessError:                                  # Notify user about error on running restart commands.
            Popen(['notify-send','Kinto: Error could not open config file!','-i','budgie-desktop-symbolic'])

    def setSysKB(self,button):
        if self.ostype == "XFCE":
            Popen(['xfce4-keyboard-settings'])
        else:
            Popen(['gnome-control-center','keyboard'])

    def setRegion(self,button):
        if self.ostype == "XFCE":
            Popen(['gnome-language-selector'])
        else:
            Popen(['gnome-control-center','region'])

    def remove_control_characters(self,s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

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

        # print(output.read())

        # the_encoding = chardet.detect(output)['encoding']
        # print(str(the_encoding) + " hello")
        # full = self.status.get_text() + op.decode('utf-8')
        # newstr = re.sub('[^A-Za-z0-9]+', '', op.decode('utf-8'))
        # print(newstr)
        status = op.decode('utf-8').rstrip()
        if "inactive" in status or "failed" in status or "deactivating" in status:
            if "journalctl" in self.command:
                stats = "<span color='red'><b>inactive</b></span>"
            else:
                stats = "<span color='yellow'><b>Debug Mode</b></span>"
        # elif "failed" in op.decode('utf-8').rstrip():
                # stats = "<span color='red'><b>failed</b></span>"
        else:
            stats = "<span color='#66ff00'><b>active</b></span>"
            # op.decode('utf-8').rstrip()
        return stats

    def remove_tags(self,raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html).strip()
        return cleantext

    def update_terminal(self):
        # subproc = self.sub_proc
        # print(self.another.get_text())
        # self.label.set_text(self.non_block_read())
        status = self.non_block_read()
        # print (self.label.get_text().strip() + ' ' + self.remove_tags(status))
        if self.label.get_text().strip() != self.remove_tags(status):
            self.label.set_markup("  " + status + "  ")
            if self.remove_tags(status) == 'active':
                self.menuitem_enable.disconnect(self.menuitem_enable.signal_id)
                self.menuitem_enable.set_active(True)
                self.menuitem_enable.signal_id = self.menuitem_enable.connect('activate',self.setEnable,False)
            else:
                self.menuitem_enable.disconnect(self.menuitem_enable.signal_id)
                self.menuitem_enable.set_active(False)
                self.menuitem_enable.signal_id = self.menuitem_enable.connect('activate',self.setEnable,True)

        return self.kinto_status.poll() is None

    # def update_terminal(self):
    #     # subproc = self.sub_proc
    #     # print(self.another.get_text())
    #     self.label.set_text(self.label.get_text() + self.non_block_read())
    #     return self.sub_proc.poll() is None

    def InputToTerm(self,cmd):
        terminal.feed_child_binary(cmd)
        print(Vte.get_minor_version())

    # def on_menu_auto(self, widget):
    #     print("add file open dialog")

    # def on_menu_enable(self, widget):
    #     print("add file open dialog")

    def on_menu_quit(self, widget):
        Gtk.main_quit()


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()

Gtk.main()