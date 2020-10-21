#!/usr/bin/env python3

from gi.repository import Gtk,GObject, Vte
from gi.repository import GLib
import os

class TheWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="inherited cell renderer")
        self.set_default_size(600, 300)
        global terminal
        terminal     = Vte.Terminal()
        terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                os.environ['HOME'],
                ["/bin/bash"],
                [],
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None,
                )

        self.button = Gtk.Button("Do The Command")
        self.button2 = Gtk.Button("End Command")
        self.command = "journalctl -f --unit=xkeysnail.service -b\n"
        self.command2 = "send \003; echo 'hello'\n"
        # expect -c "send \003;"
        self.cmdbytes = str.encode(self.command)
        self.cmdbytes2 = str.encode(self.command2)
        command = Gtk.Label("The command: "+self.command)
        self.button.connect("clicked", self.InputToTerm, self.cmdbytes)
        self.button2.connect("clicked", self.InputToTerm, self.cmdbytes2)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.button, False, True, 0)
        box.pack_start(self.button2, False, True, 0)
        box.pack_start(command, False, True, 1)
        scroller = Gtk.ScrolledWindow()
        scroller.set_hexpand(True)
        scroller.set_vexpand(True)
        scroller.add(terminal)
        box.pack_start(scroller, False, True, 2)
        self.add(box)

    def InputToTerm(self, clicker, cmd):
        terminal.feed_child_binary(cmd)
        print(Vte.get_minor_version())


win = TheWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()