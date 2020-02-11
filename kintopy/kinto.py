#!/usr/bin/env python
#
# Kinto - Python implementation of Xlib
#
# Based on code by Stephan Sokolow
# Source: https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8
from contextlib import contextmanager
import Xlib
import Xlib.display

# Connect to the X server and get the root window
disp = Xlib.display.Display()
root = disp.screen().root

# Prepare the property names we use so they can be fed into X11 APIs
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = disp.intern_atom('WM_NAME')           # Legacy encoding
NET_WM_CLASS = disp.intern_atom('_NET_WM_CLASS')  # UTF-8
WM_CLASS = disp.intern_atom('WM_CLASS')

last_seen = { 'xid': None, 'title': None }

@contextmanager
def window_obj(win_id):
    """Simplify dealing with BadWindow (make it either valid or None)"""
    window_obj = None
    if win_id:
        try:
            window_obj = disp.create_resource_object('window', win_id)
        except Xlib.error.XError:
            pass
    yield window_obj

def get_active_window():
    """Return a (window_obj, focus_has_changed) tuple for the active window."""
    win_id = root.get_full_property(NET_ACTIVE_WINDOW,Xlib.X.AnyPropertyType).value[0]

    focus_changed = (win_id != last_seen['xid'])
    if focus_changed:
        with window_obj(last_seen['xid']) as old_win:
            if old_win:
                old_win.change_attributes(event_mask=Xlib.X.NoEventMask)

        last_seen['xid'] = win_id
        with window_obj(win_id) as new_win:
            if new_win:
                new_win.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

    return win_id, focus_changed

def _get_window_class_inner(win_obj):
    for atom in (NET_WM_CLASS, WM_CLASS):
        try:
            window_class = win_obj.get_full_property(atom, 0)

        except UnicodeDecodeError:  # Apparently a Debian distro package bug
            title = "<could not decode characters>"
        else:
            if window_class:
                win_class = window_class.value.split('\x00')[1]
                if isinstance(win_class, bytes):
                    # Apparently COMPOUND_TEXT is so arcane that this is how
                    # tools like xprop deal with receiving it these days
                    win_class = win_class.split('\x00')[1].decode('latin1', 'replace')
                return win_class
            else:
                title = "<unnamed window>"

    return "{} (XID: {})".format(title, win_obj.id)

def get_window_class(win_id):
    """Look up the window name for a given X11 window ID"""
    if not win_id:
        last_seen['title'] = "<no window id>"
        return last_seen['title']

    title_changed = False
    with window_obj(win_id) as wobj:
        if wobj:
            win_title = _get_window_class_inner(wobj)
            title_changed = (win_title != last_seen['title'])
            last_seen['title'] = win_title

    return last_seen['title'], title_changed

def handle_xevent(event):
    # Loop through, ignoring events until we're notified of focus/title change
    if event.type != Xlib.X.PropertyNotify:
        return

    changed = False
    if event.atom == NET_ACTIVE_WINDOW:
        if get_active_window()[1]:
            changed = changed or get_window_class(last_seen['xid'])[1]
    elif event.atom in (NET_WM_CLASS, WM_CLASS):
        changed = changed or get_window_class(last_seen['xid'])[1]

    if changed:
        handle_change(last_seen)

def handle_change(new_state):
    """Replace this with whatever you want to actually do"""
    print(new_state['title'])

if __name__ == '__main__':
    # Listen for _NET_ACTIVE_WINDOW changes
    root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)

    # Prime last_seen with whatever window was active when we started this
    get_window_class(get_active_window()[0])
    handle_change(last_seen)

    while True:  # next_event() sleeps until we get an event
        handle_xevent(disp.next_event())