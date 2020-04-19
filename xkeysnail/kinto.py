# -*- coding: utf-8 -*-

import re
from xkeysnail.transform import *

# [Global modemap] Change modifier keys as in xmodmap
define_conditional_modmap(lambda wm_class: wm_class not in ("Gnome-terminal","konsole","io.elementary.terminal","terminator","sakura","guake","tilda","xterm","eterm","kitty"),{
    # # Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # Chromebook
    # Key.LEFT_CTRL: Key.LEFT_ALT,    # Chromebook
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # Chromebook
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,  # Chromebook

    # Default Mac/Win
    Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    Key.LEFT_CTRL: Key.LEFT_META,   # WinMac
    Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac
    Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac
    Key.RIGHT_CTRL: Key.RIGHT_META, # WinMac

    # # Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # Key.LEFT_CTRL: Key.LEFT_META,   # Mac
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac
    # Key.RIGHT_CTRL: Key.RIGHT_META, # Mac
})

# [Conditional modmap] Change modifier keys in certain applications
define_conditional_modmap(re.compile("Gnome-terminal|konsole|io.elementary.terminal|terminator|sakura|guake|tilda|xterm|eterm|kitty"), {
    # # Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,
    # # Left Ctrl Stays Left Ctrl
    # Key.LEFT_META: Key.LEFT_ALT,
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,
    # # Right Meta does not exist on chromebooks

    # Default Mac/Win
    Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    Key.LEFT_CTRL: Key.LEFT_CTRL,   # WinMac
    Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac
    Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac
    Key.RIGHT_CTRL: Key.LEFT_CTRL, # WinMac

    # # Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # # Left Ctrl Stays Left Ctrl
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac
    # Key.RIGHT_CTRL: Key.LEFT_CTRL, # Mac
})

# Keybindings for Sublime Text
# re.compile("Sublime_text")
define_keymap(re.compile("Sublime_text"),{
    # Select All Matches
    # K("M-C-g"): K("M-REFRESH"), # Chromebook
    K("Super-C-g"): K("M-F3"), # Default
}, "Sublime Text")

define_keymap(None,{
    # Cmd Tab - App Switching Default
    K("RC-Tab"): K("RC-F13"),
    K("RC-Shift-Tab"): K("RC-Shift-F13"),
    K("RC-Grave"): K("RC-Shift-F13"),
    # In-App Tab switching
    # K("M-Tab"): K("C-Tab"), # Chromebook
    # K("M-Shift-Tab"): K("C-Shift-Tab"), # Chromebook
    K("Super-Tab"): K("LC-Tab"), # Default
    K("Super-Shift-Tab"): K("LC-Shift-Tab"), # Default
    K("LC-Grave") : K("LC-Shift-Tab"), # Default

})

# define_keymap(re.compile("Gnome-terminal|io.elementary.terminal|terminator|sakura|guake|tilda|xterm|eterm|kitty"),{
#     # Ctrl Tab - In App Tab Switching
#     # LC is already set
#     K("LC-Grave") : K("LC-Shift-Tab"),
# }, "Terminals tab switching")

define_keymap(re.compile("konsole"),{
    # Ctrl Tab - In App Tab Switching
    # K("LC-Tab") : K("Shift-Right"),
    # K("LC-Shift-Tab") : K("Shift-Left"),
    K("LC-Grave") : K("Shift-Left"),

}, "Konsole tab switching")

define_keymap(re.compile("Gnome-terminal|konsole|io.elementary.terminal|terminator|sakura|guake|tilda|xterm|eterm|kitty"),{
    # Converts Cmd to use Ctrl-Shift
    K("RC-Tab"): K("RC-F13"),
    K("RC-Shift-Tab"): K("RC-Shift-F13"),
    K("RC-V"): K("C-Shift-V"),
    K("RC-MINUS"): K("C-Shift-MINUS"),
    K("RC-EQUAL"): K("C-Shift-EQUAL"),
    K("RC-BACKSPACE"): K("C-Shift-BACKSPACE"),
    K("RC-Q"): K("C-Shift-Q"),
    K("RC-W"): K("C-Shift-W"),
    K("RC-E"): K("C-Shift-E"),
    K("RC-R"): K("C-Shift-R"),
    K("RC-T"): K("C-Shift-t"),
    K("RC-Y"): K("C-Shift-Y"),
    K("RC-U"): K("C-Shift-U"),
    K("RC-I"): K("C-Shift-I"),
    K("RC-O"): K("C-Shift-O"),
    K("RC-P"): K("C-Shift-P"),
    K("RC-LEFT_BRACE"): K("C-Shift-LEFT_BRACE"),
    K("RC-RIGHT_BRACE"): K("C-Shift-RIGHT_BRACE"),
    K("RC-A"): K("C-Shift-A"),
    K("RC-S"): K("C-Shift-S"),
    K("RC-D"): K("C-Shift-D"),
    K("RC-F"): K("C-Shift-F"),
    K("RC-G"): K("C-Shift-G"),
    K("RC-H"): K("C-Shift-H"),
    K("RC-J"): K("C-Shift-J"),
    K("RC-K"): K("C-Shift-K"),
    K("RC-L"): K("C-Shift-L"),
    K("RC-SEMICOLON"): K("C-Shift-SEMICOLON"),
    K("RC-APOSTROPHE"): K("C-Shift-APOSTROPHE"),
    K("RC-GRAVE"): K("C-Shift-GRAVE"),
    K("RC-BACKSLASH"): K("C-Shift-BACKSLASH"),
    K("RC-Z"): K("C-Shift-Z"),
    K("RC-X"): K("C-Shift-X"),
    K("RC-C"): K("C-Shift-C"),
    K("RC-V"): K("C-Shift-V"),
    K("RC-B"): K("C-Shift-B"),
    K("RC-N"): K("C-Shift-N"),
    K("RC-M"): K("C-Shift-M"),
    K("RC-COMMA"): K("C-Shift-COMMA"),
    K("RC-DOT"): K("C-Shift-DOT"),
    K("RC-SLASH"): K("C-Shift-SLASH"),
    K("RC-KPASTERISK"): K("C-Shift-KPASTERISK"),
}, "terminals")

# define_keymap(re.compile("Chromium-browser"),{
#     # K("RC-Tab"): K("C-F13"),
#     # K("RC-Shift-Tab"): K("C-f1"),
# }, "Chromium-browser")
