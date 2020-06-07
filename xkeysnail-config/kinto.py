# -*- coding: utf-8 -*-

import re
from xkeysnail.transform import *

# Use the following for testing terminal keymaps
# terminals = [ "", ... ]
# xbindkeys -mk
terminals = ["gnome-terminal","konsole","io.elementary.terminal","terminator","sakura","guake","tilda","xterm","eterm","kitty","alacritty","mate-terminal","tilix","xfce4-terminal"]
terminals = [term.casefold() for term in terminals]
termStr = "|".join(str(x) for x in terminals)

mscodes = ["code","vscodium"]
codeStr = "|".join(str(x) for x in mscodes)

# [Global modemap] Change modifier keys as in xmodmap
define_conditional_modmap(lambda wm_class: wm_class.casefold() not in terminals,{
    # # Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # Chromebook
    # Key.LEFT_CTRL: Key.LEFT_ALT,    # Chromebook
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # Chromebook
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,  # Chromebook

    # # Default Mac/Win
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    # Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    # Key.LEFT_CTRL: Key.LEFT_META,   # WinMac
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac
    # Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac
    # Key.RIGHT_CTRL: Key.RIGHT_META, # WinMac

    # # KintoWin
    # Key.LEFT_CTRL: Key.RIGHT_CTRL,   # KintoWin

    # # Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # Key.LEFT_CTRL: Key.LEFT_META,   # Mac
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac
    # Key.RIGHT_CTRL: Key.RIGHT_META, # Mac
})

# [Conditional modmap] Change modifier keys in certain applications
define_conditional_modmap(re.compile(termStr, re.IGNORECASE), {
    # # Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,     # Chromebook
    # # Left Ctrl Stays Left Ctrl
    # Key.LEFT_META: Key.LEFT_ALT,      # Chromebook
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,    # Chromebook - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,    # Chromebook
    # # Right Meta does not exist on chromebooks

    # # Default Mac/Win
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    # Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    # Key.LEFT_CTRL: Key.LEFT_CTRL,   # WinMac
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac - Multi-language (Remove)
    # Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac
    # Key.RIGHT_CTRL: Key.LEFT_CTRL,  # WinMac

    # # KintoWin
    # Key.LEFT_CTRL: Key.RIGHT_CTRL,   # KintoWin
    # Key.LEFT_META: Key.LEFT_CTRL,    # KintoWin

    # # Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # # Left Ctrl Stays Left Ctrl
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac
    # Key.RIGHT_CTRL: Key.LEFT_CTRL,  # Mac
})

# Keybindings for Nautilus
define_keymap(re.compile("org.gnome.nautilus", re.IGNORECASE),{
    K("RC-Up"): K("M-Up"),          # Go Up dir
    K("RC-Down"): K("M-Down"),      # Go Down dir
    K("RC-Left"): K("M-Left"),      # Go Back
    K("RC-Right"): K("M-Right"),    # Go Forward
})

define_keymap(None,{
    # Basic App hotkey functions
    K("RC-Q"): K("Alt-F4"),
    K("RC-H"): K("Alt-F9"),
    # Cmd Tab - App Switching Default
    K("RC-Tab"): K("RC-F13"),                     # Default not-xfce4
    K("RC-Shift-Tab"): K("RC-Shift-F13"),         # Default not-xfce4
    K("RC-Grave"): K("M-F6"),                     # Default not-xfce4
    K("RC-Shift-Grave"): K("M-Shift-F6"),         # Default not-xfce4
    # K("RC-Tab"): K("RC-backslash"),               # xfce4
    # K("RC-Shift-Tab"): K("RC-Shift-backslash"),   # xfce4
    # K("RC-Grave"): K("RC-Shift-backslash"),       # xfce4
    # In-App Tab switching
    # K("M-Tab"): K("C-Tab"),                       # Chromebook - In-App Tab switching
    # K("M-Shift-Tab"): K("C-Shift-Tab"),           # Chromebook - In-App Tab switching
    # K("M-Grave") : K("C-Shift-Tab"),              # Chromebook - In-App Tab switching
    K("Super-Tab"): K("LC-Tab"),                  # Default not-chromebook
    K("Super-Shift-Tab"): K("LC-Shift-Tab"),      # Default not-chromebook

    # Wordwise
    K("RC-Left"): K("Home"),                      # Beginning of Line
    K("Super-a"): K("Home"),                      # Beginning of Line
    K("RC-Shift-Left"): K("Shift-Home"),          # Select all to Beginning of Line
    K("RC-Right"): K("End"),                      # End of Line
    K("Super-e"): K("End"),                       # End of Line
    K("RC-Shift-Right"): K("Shift-End"),          # Select all to End of Line
    # K("RC-Left"): K("C-LEFT_BRACE"),              # Firefox-nw - Back
    # K("RC-Right"): K("C-RIGHT_BRACE"),            # Firefox-nw - Forward
    # K("RC-Left"): K("M-LEFT"),                    # Chrome-nw - Back
    # K("RC-Right"): K("M-RIGHT"),                  # Chrome-nw - Forward
    K("RC-Up"): K("C-Home"),                      # Beginning of File
    K("RC-Shift-Up"): K("C-Shift-Home"),          # Select all to Beginning of File
    K("RC-Down"): K("C-End"),                     # End of File
    K("RC-Shift-Down"): K("C-Shift-End"),         # Select all to End of File
    # K("M-Backspace"): K("Delete"),                # Chromebook - Delete
    K("Super-Backspace"): K("C-Backspace"),       # Default not-chromebook - Delete Left Word of Cursor
    K("Super-Delete"): K("C-Delete"),             # Default not-chromebook - Delete Right Word of Cursor
    K("Alt-Backspace"): K("C-Backspace"),       # Default not-chromebook - Delete Left Word of Cursor
    K("Alt-Delete"): K("C-Delete"),             # Default not-chromebook - Delete Right Word of Cursor
    # K(""): pass_through_key,                      # cancel
    # K(""): K(""),                                 #
})

define_keymap(lambda wm_class: wm_class.casefold() not in mscodes,{
    # Wordwise remaining - for Everything but VS Code
    K("M-Left"): K("C-Left"),               # Left of Word
    K("M-Shift-Left"): K("C-Shift-Left"),   # Select Left of Word
    K("M-Right"): K("C-Right"),             # Right of Word
    K("M-Shift-Right"): K("C-Shift-Right"), # Select Right of Word
    # ** VS Code fix **
    #   Electron issue precludes normal keybinding fix.
    #   Alt menu auto-focus/toggle gets in the way.
    #
    #   refer to ./xkeysnail-config/vscode_keybindings.json
    # **
    #
    # ** Firefox fix **
    #   User will need to set "ui.key.menuAccessKeyFocuses"
    #   under about:config to false.
    #
    #   https://superuser.com/questions/770301/pentadactyl-how-to-disable-menu-bar-toggle-by-alt
    # **
    #
})

# Keybindings for VS Code
define_keymap(re.compile(codeStr, re.IGNORECASE),{
    # Wordwise remaining - for VS Code
    # Alt-F19 hack fixes Alt menu activation
    K("M-Left"): [K("M-F19"),K("C-Left")],                  # Left of Word
    K("M-Right"): [K("M-F19"),K("C-Right")],                # Right of Word
    K("M-Shift-Left"): [K("M-F19"),K("C-Shift-Left")],      # Select Left of Word
    K("M-Shift-Right"): [K("M-F19"),K("C-Shift-Right")],    # Select Right of Word
    
    # K("C-PAGE_DOWN"): pass_through_key,         # cancel next_view
    # K("C-PAGE_UP"): pass_through_key,           # cancel prev_view
    K("C-M-Left"): K("C-PAGE_UP"),              # next_view
    K("C-M-Right"): K("C-PAGE_DOWN"),           # prev_view

    # VS Code Shortcuts
    K("C-g"): pass_through_key,                 # cancel Go to Line...
    K("Super-g"): K("C-g"),                     # Go to Line...
    K("F3"): pass_through_key,                  # cancel Find next
    K("C-h"): pass_through_key,                 # cancel replace
    K("C-M-f"): K("C-h"),                       # replace
    K("C-Shift-h"): pass_through_key,           # cancel replace_next
    K("C-M-e"): K("C-Shift-h"),                 # replace_next
    K("f3"): pass_through_key,                  # cancel find_next
    K("C-g"): K("f3"),                          # find_next
    K("Shift-f3"): pass_through_key,            # cancel find_prev
    K("C-Shift-g"): K("Shift-f3"),              # find_prev
    # K("Super-C-g"): K("C-f2"),                  # Default - Sublime - find_all_under
    # K("C-M-g"): K("C-f2"),                      # Chromebook - Sublime - find_all_under
    # K("Super-Shift-up"): K("M-Shift-up"),       # multi-cursor up - Sublime
    # K("Super-Shift-down"): K("M-Shift-down"),   # multi-cursor down - Sublime
    # K(""): pass_through_key,                    # cancel
    # K(""): K(""),                               #
}, "Code")

# Keybindings for Sublime Text
define_keymap(re.compile("Sublime_text", re.IGNORECASE),{
    K("C-Super-up"): K("M-o"),                  # Switch file
    K("Super-RC-f"): K("f11"),                  # toggle_full_screen
    K("C-M-v"): [K("C-k"), K("C-v")],           # paste_from_history
    K("C-up"): pass_through_key,                # cancel scroll_lines up
    K("Super-M-up"): K("C-up"),                 # scroll_lines up
    K("C-down"): pass_through_key,              # cancel scroll_lines down
    K("Super-M-down"): K("C-down"),             # scroll_lines down
    K("Super-Shift-up"): K("M-Shift-up"),       # multi-cursor up
    K("Super-Shift-down"): K("M-Shift-down"),   # multi-cursor down
    K("C-PAGE_DOWN"): pass_through_key,         # cancel next_view
    K("C-PAGE_UP"): pass_through_key,           # cancel prev_view
    K("C-Shift-left_brace"): K("C-PAGE_DOWN"),  # next_view
    K("C-Shift-right_brace"): K("C-PAGE_UP"),   # prev_view
    K("C-M-right"): K("C-PAGE_DOWN"),           # next_view
    K("C-M-left"): K("C-PAGE_UP"),              # prev_view
    K("insert"): pass_through_key,              # cancel toggle_overwrite
    K("C-M-o"): K("insert"),                    # toggle_overwrite
    K("M-c"): pass_through_key,                 # cancel toggle_case_sensitive
    K("C-M-c"): K("M-c"),                       # toggle_case_sensitive
    K("C-h"): pass_through_key,                 # cancel replace
    K("C-M-f"): K("C-h"),                       # replace
    K("C-Shift-h"): pass_through_key,           # cancel replace_next
    K("C-M-e"): K("C-Shift-h"),                 # replace_next
    K("f3"): pass_through_key,                  # cancel find_next
    K("C-g"): K("f3"),                          # find_next
    K("Shift-f3"): pass_through_key,            # cancel find_prev
    K("C-Shift-g"): K("Shift-f3"),              # find_prev
    K("C-f3"): pass_through_key,                # cancel find_under
    K("Super-M-g"): K("C-f3"),                  # find_under
    K("C-Shift-f3"): pass_through_key,          # cancel find_under_prev
    K("Super-M-Shift-g"): K("C-Shift-f3"),      # find_under_prev
    K("M-f3"): pass_through_key,                # Default - cancel find_all_under
    # K("M-Refresh"): pass_through_key,           # Chromebook - cancel find_all_under
    # K("M-C-g"): K("M-Refresh"),                 # Chromebook - find_all_under
    K("Super-C-g"): K("M-f3"),                  # Default - find_all_under
    K("C-Shift-up"): pass_through_key,          # cancel swap_line_up
    K("Super-C-up"): K("C-Shift-up"),           # swap_line_up
    K("C-Shift-down"): pass_through_key,        # cancel swap_line_down
    K("Super-C-down"): K("C-Shift-down"),       # swap_line_down
    K("C-Pause"): pass_through_key,             # cancel cancel_build
    K("Super-c"): K("C-Pause"),                 # cancel_build
    K("f9"): pass_through_key,                  # cancel sort_lines case_s false
    K("f5"): K("f9"),                           # sort_lines case_s false
    K("Super-f9"): pass_through_key,            # cancel sort_lines case_s true
    K("Super-f5"): K("Super-f9"),               # sort_lines case_s true
    K("M-Shift-Key_1"): pass_through_key,       # cancel set_layout
    K("C-M-Key_1"): K("M-Shift-Key_1"),         # set_layout
    K("M-Shift-Key_2"): pass_through_key,       # cancel set_layout
    K("C-M-Key_2"): K("M-Shift-Key_2"),         # set_layout
    K("M-Shift-Key_3"): pass_through_key,       # cancel set_layout
    K("C-M-Key_3"): K("M-Shift-Key_3"),         # set_layout
    K("M-Shift-Key_4"): pass_through_key,       # cancel set_layout
    K("C-M-Key_4"): K("M-Shift-Key_4"),         # set_layout
    K("M-Shift-Key_8"): pass_through_key,       # cancel set_layout
    K("C-M-Shift-Key_2"): K("M-Shift-Key_8"),   # set_layout
    K("M-Shift-Key_9"): pass_through_key,       # cancel set_layout
    K("C-M-Shift-Key_3"): K("M-Shift-Key_9"),   # set_layout
    K("M-Shift-Key_5"): pass_through_key,       # cancel set_layout
    K("C-M-Shift-Key_5"): K("M-Shift-Key_5"),   # set_layout
    # K(""): pass_through_key,                    # cancel
    # K(""): K(""),                               #
}, "Sublime Text")

define_keymap(re.compile("konsole", re.IGNORECASE),{
    # Ctrl Tab - In App Tab Switching
    K("LC-Tab") : K("Shift-Right"),
    K("LC-Shift-Tab") : K("Shift-Left"),
    K("LC-Grave") : K("Shift-Left"),

}, "Konsole tab switching")

define_keymap(re.compile("Io.elementary.terminal|kitty", re.IGNORECASE),{
    # Ctrl Tab - In App Tab Switching
    K("LC-Tab") : K("LC-Shift-Right"),
    K("LC-Shift-Tab") : K("LC-Shift-Left"),
    K("LC-Grave") : K("LC-Shift-Left"),

}, "Elementary Terminal tab switching")

define_keymap(re.compile(termStr, re.IGNORECASE),{
    # Ctrl Tab - In App Tab Switching
    K("LC-Tab") : K("LC-PAGE_DOWN"),
    K("LC-Shift-Tab") : K("LC-PAGE_UP"),
    K("LC-Grave") : K("LC-PAGE_UP"),
    # Converts Cmd to use Ctrl-Shift
    K("RC-Tab"): K("RC-F13"),
    K("RC-Shift-Tab"): K("RC-Shift-F13"),
    K("RC-V"): K("C-Shift-V"),
    K("RC-MINUS"): K("C-Shift-MINUS"),
    K("RC-EQUAL"): K("C-Shift-EQUAL"),
    K("RC-BACKSPACE"): K("C-Shift-BACKSPACE"),
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
