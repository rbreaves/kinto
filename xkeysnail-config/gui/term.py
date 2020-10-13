#!/usr/bin/env python3
import gi
# import textwrap
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GObject

import os
from subprocess import Popen, PIPE
import fcntl

wnd = Gtk.Window()
wnd.set_default_size(400, 400)
wnd.connect("destroy", Gtk.main_quit)
sw = Gtk.ScrolledWindow()
label = Gtk.Label()
label.set_alignment(0, 0)
label.set_selectable(True)
label.set_line_wrap(True)
label.set_max_width_chars(150)
sw.add_with_viewport(label)
wnd.add(sw)
wnd.show_all()
sub_proc = Popen("journalctl -f --unit=xkeysnail.service -b", stdout=PIPE, shell=True)
# sub_proc2 = Popen('fold', stdin=sub_proc.stdout, stdout=PIPE)
# sub_proc2.communicate()
sub_outp = ""


def non_block_read(output):
    ''' even in a thread, a normal read with block until the buffer is full '''
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    op = output.read()
    if op == None:
        return ''
    return op.decode('utf-8')

# def wrap(s, w):
#     return textwrap.fill(s, w)
# def wrap(s, w):
#     return [s[i:i + w] for i in range(0, len(s), w)]

def update_terminal():
    # wrapper = textwrap.TextWrapper(width=50) 
    # word_list = wrapper.wrap(text=sub_proc.stdout)
    label.set_text(label.get_text() + non_block_read(sub_proc.stdout))
    return sub_proc.poll() is None

GObject.timeout_add(100, update_terminal)
Gtk.main()