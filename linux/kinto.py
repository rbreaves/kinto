# -*- coding: utf-8 -*-
# autostart = true

import re
from xkeysnail.transform import *

# Use the following for testing terminal keymaps
# terminals = [ "", ... ]
# xbindkeys -mk
terminals = ["kinto-gui.py","gnome-terminal","konsole","io.elementary.terminal","terminator","sakura","guake","tilda","xterm","eterm","kitty","alacritty","mate-terminal","tilix","xfce4-terminal","hyper"]
terminals = [term.casefold() for term in terminals]
termStr = "|".join(str(x) for x in terminals)

mscodes = ["code","vscodium"]
codeStr = "|".join(str(x) for x in mscodes)

# Add remote desktop clients & VM software here
# Ideally we'd only exclude the client window,
# but that may not be easily done.
remotes = ["org.remmina.Remmina","xfreerdp"]
remotes = [client.casefold() for client in remotes]

# Add remote desktop clients & VMs for no remapping
terminals.extend(remotes)
mscodes.extend(remotes)

# Use for browser specific hotkeys
browsers = ["Chromium","Chromium-browser","Google-chrome","microsoft-edge-dev","microsoft-edge","Epiphany","Firefox","Discord"]
browsers = [browser.casefold() for browser in browsers]
browserStr = "|".join(str(x) for x in browsers)

chromes = ["Chromium","Chromium-browser","Google-chrome","microsoft-edge-dev","microsoft-edge"]
chromes = [chrome.casefold() for chrome in chromes]
chromeStr = "|".join(str(x) for x in chromes)

# edges = ["microsoft-edge-dev","microsoft-edge"]
# edges = [edge.casefold() for edge in edges]
# edgeStr = "|".join(str(x) for x in edges)

define_multipurpose_modmap(
    # {Key.ENTER: [Key.ENTER, Key.RIGHT_CTRL]   # Enter2Cmd
    # {Key.CAPSLOCK: [Key.ESC, Key.RIGHT_CTRL]  # Caps2Esc
    # {Key.LEFT_META: [Key.ESC, Key.RIGHT_CTRL] # Caps2Esc - Chromebook
    {                                         # Placeholder
})

# Fix for avoiding modmapping when using Synergy keyboard/mouse sharing.
# Synergy doesn't set a wm_class, so this may cause issues with other
# applications that also don't set the wm_class.
# Enable only if you use Synergy.
# define_conditional_modmap(lambda wm_class: wm_class == '', {})

# [Global modemap] Change modifier keys as in xmodmap
define_conditional_modmap(lambda wm_class: wm_class.casefold() not in terminals,{

    # Key.CAPSLOCK: Key.RIGHT_CTRL,   # Caps2Cmd
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Caps2Cmd - Chromebook

    # - IBM
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # IBM
    # Key.LEFT_CTRL: Key.LEFT_ALT,    # IBM
    # Key.CAPSLOCK: Key.LEFT_META,    # IBM
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # IBM - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,  # IBM - Multi-language (Remove)

    # - Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # Chromebook
    # Key.LEFT_CTRL: Key.LEFT_ALT,    # Chromebook
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # Chromebook - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,  # Chromebook - Multi-language (Remove)

    # - Default Mac/Win
    # - Default Win
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    # Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    # Key.LEFT_CTRL: Key.LEFT_META,   # WinMac
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac - Multi-language (Remove)
    # Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_META, # WinMac - Multi-language (Remove)

    # - Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # Key.LEFT_CTRL: Key.LEFT_META,   # Mac
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_META, # Mac - Multi-language (Remove)
})

# [Conditional modmap] Change modifier keys in certain applications
define_conditional_modmap(re.compile(termStr, re.IGNORECASE), {
    # - IBM
    # Key.LEFT_ALT: Key.RIGHT_CTRL,     # IBM
    # # Left Ctrl Stays Left Ctrl
    # Key.CAPSLOCK: Key.LEFT_ALT,       # IBM
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,    # IBM - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,    # IBM
    # # Right Meta does not exist on chromebooks
    
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # IBM - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,  # IBM - Multi-language (Remove)

    # - Chromebook
    # Key.LEFT_ALT: Key.RIGHT_CTRL,     # Chromebook
    # # Left Ctrl Stays Left Ctrl
    # Key.LEFT_META: Key.LEFT_ALT,      # Chromebook
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,    # Chromebook - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.RIGHT_ALT,    # Chromebook
    # # Right Meta does not exist on chromebooks

    # - Default Mac/Win
    # - Default Win
    # Key.LEFT_ALT: Key.RIGHT_CTRL,   # WinMac
    # Key.LEFT_META: Key.LEFT_ALT,    # WinMac
    # Key.LEFT_CTRL: Key.LEFT_CTRL,   # WinMac
    # Key.RIGHT_ALT: Key.RIGHT_CTRL,  # WinMac - Multi-language (Remove)
    # Key.RIGHT_META: Key.RIGHT_ALT,  # WinMac - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.LEFT_CTRL,  # WinMac - Multi-language (Remove)

    # - Mac Only
    # Key.LEFT_META: Key.RIGHT_CTRL,  # Mac
    # # Left Ctrl Stays Left Ctrl
    # Key.RIGHT_META: Key.RIGHT_CTRL, # Mac - Multi-language (Remove)
    # Key.RIGHT_CTRL: Key.LEFT_CTRL,  # Mac - Multi-language (Remove)
})

# Keybindings for IntelliJ
define_keymap(re.compile("^jetbrains-(?!.*toolbox).*$", re.IGNORECASE),{
    # General
    K("C-Key_0"): K("M-Key_0"),                 # Open corresponding tool window
    K("C-Key_1"): K("M-Key_1"),                 # Open corresponding tool window
    K("C-Key_2"): K("M-Key_2"),                 # Open corresponding tool window
    K("C-Key_3"): K("M-Key_3"),                 # Open corresponding tool window
    K("C-Key_4"): K("M-Key_4"),                 # Open corresponding tool window
    K("C-Key_5"): K("M-Key_5"),                 # Open corresponding tool window
    K("C-Key_6"): K("M-Key_6"),                 # Open corresponding tool window
    K("C-Key_7"): K("M-Key_7"),                 # Open corresponding tool window
    K("C-Key_8"): K("M-Key_8"),                 # Open corresponding tool window
    K("C-Key_9"): K("M-Key_9"),                 # Open corresponding tool window
    K("Super-Grave"): K("C-Grave"),             # Quick switch current scheme
    K("C-Comma"): K("C-M-s"),                   # Open Settings dialog
    K("C-Semicolon"): K("C-M-Shift-s"),         # Open Project Structure dialog
    # Debugging
    K("C-M-r"): K("F9"),                        # Resume program
    # Search/Replace
    K("C-g"): K("F3"),                          # Find next
    K("C-Shift-F3"): K("Shift-F3"),             # Find previous
    K("Super-g"): K("M-j"),                     # Select next occurrence
    K("C-Super-g"): K("C-M-Shift-j"),           # Select all occurrences
    K("Super-Shift-g"): K("M-Shift-j"),         # Unselect occurrence
    # Editing
    K("Super-Space"): K("LC-Space"),            # Basic code completion
    K("Super-Shift-Space"): K("LC-Shift-Space"),# Smart code completion
    K("Super-j"): K("C-q"),                     # Quick documentation lookup
    K("C-n"): K("M-Insert"),                    # Generate code...
    K("Super-o"): K("C-o"),                     # Override methods
    K("Super-i"): K("C-i"),                     # Implement methods
    K("M-Up"): K("C-w"),                        # Extend selection
    K("M-Down"): K("C-Shift-w"),                # Shrink selection
    K("Super-Shift-q"): K("M-q"),               # Context info
    K("Super-M-o"): K("C-M-o"),                 # Optimize imports
    K("Super-M-i"): K("C-M-i"),                 # Auto-indent line(s)
    K("C-Backspace"): K("C-y"),                 # Delete line at caret
    K("Super-Shift-j"): K("C-Shift-j"),         # Smart line join
    K("M-Delete"): K("C-Delete"),               # Delete to word end
    K("M-Backspace"): K("C-Backspace"),         # Delete to word start
    K("C-Shift-Equal"): K("C-KPPLUS"),          # Expand code block
    K("C-Minus"): K("C-KPMINUS"),               # Collapse code block
    K("C-Shift-Equal"): K("C-Shift-KPPLUS"),    # Expand all
    K("C-Shift-Minus"): K("C-Shift-KPMINUS"),   # Collapse all
    K("C-w"): K("C-F4"),                        # Close active editor tab
    # Refactoring
    K("C-Delete"): K("M-Delete"),               # Safe Delete
    K("C-T"): K("C-M-Shift-t"),                 # Refactor this
    # Navigation
    K("C-o"): K("C-n"),                         # Go to class
    K("C-Shift-o"): K("C-Shift-n"),             # Go to file
    K("C-M-o"): K("C-M-Shift-n"),               # Go to symbol
    K("Super-Right"): K("M-Right"),             # Go to next editor tab
    K("Super-Left"): K("M-Left"),               # Go to previous editor tab
    K("Super-l"): K("C-g"),                     # Go to line
    K("Super-e"): K("C-e"),                     # Recent files popup
    K("M-Space"): K("C-Shift-i"),               # Open quick definition lookup
    K("C-Y"): K("C-Shift-i"),                   # Open quick definition lookup
    K("Super-Shift-b"): K("C-Shift-b"),         # Go to type declaration
    K("Super-Up"): K("M-Up"),                   # Go to previous
    K("Super-Down"): K("M-Down"),               # Go to next method
    K("Super-h"): K("C-h"),                     # Type hierarchy
    K("Super-M-h"): K("C-M-h"),                 # Call hierarchy
    K("C-Down"): K("C-Enter"),                  # Edit source/View source
    K("M-Home"): K("M-Home"),                   # Show navigation bar
    K("F2"): K("F11"),                          # Toggle bookmark
    K("Super-F3"): K("C-F11"),                  # Toggle bookmark with mnemonic
    K("Super-Key_0"): K("C-Key_0"),             # Go to numbered bookmark
    K("Super-Key_1"): K("C-Key_1"),             # Go to numbered bookmark
    K("Super-Key_2"): K("C-Key_2"),             # Go to numbered bookmark
    K("Super-Key_3"): K("C-Key_3"),             # Go to numbered bookmark
    K("Super-Key_4"): K("C-Key_4"),             # Go to numbered bookmark
    K("Super-Key_5"): K("C-Key_5"),             # Go to numbered bookmark
    K("Super-Key_6"): K("C-Key_6"),             # Go to numbered bookmark
    K("Super-Key_7"): K("C-Key_7"),             # Go to numbered bookmark
    K("Super-Key_8"): K("C-Key_8"),             # Go to numbered bookmark
    K("Super-Key_9"): K("C-Key_9"),             # Go to numbered bookmark
    K("C-F3"): K("Shift-F11"),                  # Show bookmarks
    # Compile and Run
    K("Super-M-r"): K("M-Shift-F10"),           # Select configuration and run
    K("Super-M-d"): K("M-Shift-F9"),            # Select configuration and debug
    K("Super-r"): K("Shift-F10"),               # Run
    K("Super-d"): K("Shift-F9"),                # Debug
    K("Super-Shift-r"): K("C-Shift-F10"),       # Run context configuration from editor
    K("Super-Shift-d"): K("C-Shift-F9"),        # Debug context configuration from editor
    # VCS/Local History
    K("Super-v"): K("M-Grave"),                 # VCS quick popup
    K("Super-c"): K("LC-c"),                    # Sigints - interrupt
})

##########################################
# START OF FILE MANAGER GROUP OF KEYMAPS #
##########################################

# Keybindings overrides for Caja 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("caja", re.IGNORECASE),{
    # K("RC-Super-o"): K("RC-Shift-Enter"),   # Open in new tab 
    K("RC-Super-o"): K("RC-Shift-W"),       # Open in new window
},"Overrides_Caja")

# Keybindings overrides for Dolphin 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("dolphin", re.IGNORECASE),{
    K("RC-Super-o"): K("RC-Shift-o"), # Open in new window (or new tab, user's choice)
    # "Open in new window" requires manually setting custom shortcut of Ctrl+Shift+o 
    # in Dolphin's keyboard shortcuts. There is no default shortcut set for this function.
    ### 
    # "Open in new tab" requires manually setting custom shortcut of Ctrl+Shift+o in 
    # Dolphin's keyboard shortcuts. There is no default shortcut set for this function. 
    ### 
    K("RC-Shift-N"): K("F10"),                  # Create new folder
    K("RC-comma"): K("RC-Shift-comma"),         # Open preferences dialog
},"Overrides_Dolphin")

# Keybindings overrides for elementary OS Files 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("io.elementary.files", re.IGNORECASE),{
    # K("RC-Super-o"): K("Shift-Enter"),          # Open folder in new tab
    K("RC-Comma"): None,                        # Disable preferences shortcut since none availabe
},"Overrides_Pantheon")

# Keybindings overrides for Nautilus 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("org.gnome.Nautilus", re.IGNORECASE),{
    K("RC-Super-o"): K("Shift-Enter"),           # Open in new window
    # K("RC-Super-o"): K("RC-Enter"),                 # Open in new tab
    K("RC-comma"): K("RC-comma"),                   # Overrides "Open preferences dialog" shortcut below
},"Overrides_Nautilus")

# Keybindings overrides for PCManFM 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("pcmanfm", re.IGNORECASE),{
    K("RC-Backspace"): [K("Delete"),K("Enter")],    # Move to Trash (delete, bypass dialog)
},"Overrides_PCManFM")

# Keybindings overrides for SpaceFM
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("spacefm", re.IGNORECASE),{
    K("RC-Shift-N"): [K("RC-F")],	                # Create new folder is Ctrl+F by default
    K("RC-Backspace"): [K("Delete"),K("Enter")],	# Move to Trash (delete, bypass dialog)
    K("RC-comma"): [K("M-V"),K("p")],               # Overrides "Open preferences dialog" shortcut below
    # This shortcut ^^^^^^^^^^^^^^^ is not fully working in SpaceFM. Opens "View" menu but not Preferences. 
    # SpaceFM seems to be doing some nasty binding that blocks things like Alt+Tab while the menu is open. 
},"Overrides_SpaceFM")

# Keybindings overrides for Thunar 
# (overrides some bindings from general file browser code block below)
define_keymap(re.compile("thunar", re.IGNORECASE),{
    K("RC-Super-o"): K("RC-Shift-P"),          # Open in new tab
    K("RC-comma"): [K("M-E"),K("E")],          # Overrides "Open preferences dialog" shortcut below
},"Overrides_Thunar")

filemanagers = [
    "caja",
    "dolphin",
    "io.elementary.files",
    "nemo",
    "org.gnome.Nautilus",
    "pcmanfm",
    "pcmanfm-qt",
    "spacefm",
    "thunar",
]
filemanagers = [filemanager.casefold() for filemanager in filemanagers]
filemanagerStr = "|".join(str(x) for x in filemanagers)

# Keybindings for general file browsers group: 
# 
# Caja File Browser (MATE file manager, fork of Nautilus)
# Dolphin (KDE file manager)
# Nautilus (GNOME file manager, may be called "Files")
# Nemo (Cinnamon file manager, fork of Nautilus, may be called "Files")
# Pantheon Files (elementary OS file manager, may be called "Files")
# PCManFM (LXDE file manager)
# PCManFM-Qt (LXQt file manager)
# SpaceFM (Fork of PCManFM file manager)
# Thunar File Manager (Xfce file manager)
# 
define_keymap(re.compile(filemanagerStr, re.IGNORECASE),{
    K("RC-i"): K("M-Enter"),                # File properties dialog (Get Info)
    K("RC-comma"): [K("M-E"),K("N")],       # Open preferences dialog
    K("RC-Up"): K("M-Up"),                  # Go Up dir
    # K("RC-Down"): K("M-Down"),            # Go Down dir (only works on folders)
    # K("RC-Down"): K("RC-O"),              # Go Down dir (open folder/file)
    K("RC-Down"): K("Enter"),               # Go Down dir (open folder/file)
    # K("RC-Shift-Down"): K("RC-Shift-o"),  # Open in new window (doesn't match Finder)
    K("RC-Super-o"): K("RC-Shift-o"),       # Open in new window
    K("RC-Left"): K("M-Left"),              # Go Back
    K("RC-Right"): K("M-Right"),            # Go Forward
    # To enable renaming files with the Enter key, uncomment the two lines just below. 
    # Use Ctrl+Shift+Enter to escape or activate text fields. 
    # K("Enter"): K("F2"),				    # Rename with Enter key
    # K("RC-Shift-Enter"): K("Enter"),	    # Remap alternative "Enter" key to easily activate/exit text fields
    K("RC-Shift-dot"): K("RC-H"),           # Show/hide hidden files ("dot" files)
    K("RC-Backspace"): K("Delete"),	        # Move to Trash (delete)
    K("RC-D"): [K("RC-C"),K("RC-V")],       # Mimic Finder's Duplicate command (Copy, then Paste)
},"File_Managers")

########################################
# END OF FILE MANAGER GROUP OF KEYMAPS #
########################################

# Keybindings for Browsers
define_keymap(re.compile(browserStr, re.IGNORECASE),{
    K("RC-Q"): K("RC-Q"),           # Close all browsers Instances
    K("M-RC-I"): K("RC-Shift-I"),   # Dev tools
    K("M-RC-J"): K("RC-Shift-J"),   # Dev tools
    K("RC-Key_1"): K("M-Key_1"),    # Jump to Tab #1-#8
    K("RC-Key_2"): K("M-Key_2"),
    K("RC-Key_3"): K("M-Key_3"),
    K("RC-Key_4"): K("M-Key_4"),
    K("RC-Key_5"): K("M-Key_5"),
    K("RC-Key_6"): K("M-Key_6"),
    K("RC-Key_7"): K("M-Key_7"),
    K("RC-Key_8"): K("M-Key_8"),
    K("RC-Key_9"): K("M-Key_9"),    # Jump to last tab
})

# Open preferences in browsers
define_keymap(re.compile("Firefox", re.IGNORECASE),{
    K("C-comma"): [K("C-T"),K("a"),K("b"),K("o"),K("u"),K("t"),K("Shift-SEMICOLON"),K("p"),K("r"),K("e"),K("f"),K("e"),K("r"),K("e"),K("n"),K("c"),K("e"),K("s"),K("Enter")],
})
define_keymap(re.compile(chromeStr, re.IGNORECASE),{
    K("C-comma"): [K("M-e"), K("s"),K("Enter")],
})
# Opera C-F12

# None referenced here originally
# - but remote clients and VM software ought to be set here
# These are the typical remaps for ALL GUI based apps
define_keymap(lambda wm_class: wm_class.casefold() not in remotes,{
    K("RC-Space"): K("Alt-F1"),                   # Default SL - Launch Application Menu (gnome/kde)
    K("RC-F3"):K("Super-d"),                      # Default SL - Show Desktop (gnome/kde,eos)
    K("RC-Super-f"):K("M-F10"),                      # Default SL - Maximize app (gnome/kde)
    # K("Super-Right"):K("C-M-Right"),              # Default SL - Change workspace (budgie)
    # K("Super-Left"):K("C-M-Left"),                # Default SL - Change workspace (budgie)
    K("RC-Q"): K("M-F4"),                         # Default SL - not-popos
    K("RC-H"):K("Super-h"),                       # Default SL - Minimize app (gnome/budgie/popos/fedora)
    K("M-Tab"): pass_through_key,                 # Default not-xfce4 - Cmd Tab - App Switching Default
    K("RC-Tab"): K("M-Tab"),                      # Default not-xfce4 - Cmd Tab - App Switching Default
    K("RC-Shift-Tab"): K("M-Shift-Tab"),          # Default not-xfce4 - Cmd Tab - App Switching Default
    K("RC-Grave"): K("M-Grave"),                  # Default not-xfce4 - Cmd ` - Same App Switching
    K("RC-Shift-Grave"): K("M-Shift-Grave"),      # Default not-xfce4 - Cmd ` - Same App Switching
    # K("Super-Right"):K("Super-Page_Up"),          # SL - Change workspace (ubuntu/fedora)
    # K("Super-Left"):K("Super-Page_Down"),         # SL - Change workspace (ubuntu/fedora)
    # K("Super-Right"):K("Super-C-Up"),             # SL - Change workspace (popos)
    # K("Super-Left"):K("Super-C-Down"),            # SL - Change workspace (popos)
    # K("RC-Q"):K("Super-q"),                       # SL - Close Apps (popos)
    # K("RC-Space"): K("Super-Space"),              # SL - Launch Application Menu (eos)
    # K("RC-H"): K("Super-Page_Down"),              # SL - Minimize app (kde_neon)
                                                  # SL - Default SL - Change workspace (kde_neon)
    # K("RC-Space"): K("LC-Esc"),                   # SL- Launch Application Menu xfce4
    # K("RC-F3"):K("C-M-d"),                        # SL- Show Desktop xfce4
    # K("RC-LC-f"):K("Super-Up"),                   # SL- Maximize app eos
    # K("RC-LC-f"):K("Super-PAGE_UP"),              # SL- Maximize app manjaro
    # Basic App hotkey functions
    # K("RC-H"):K("M-F9"),                          # SL - Minimize app xfce4
    # K("RC-LC-f"):K("Super-PAGE_DOWN"),            # SL - Minimize app manjaro
    # Cmd Tab - App Switching Default
    # K("RC-Tab"): K("RC-backslash"),               # xfce4
    # K("RC-Shift-Tab"): K("RC-Shift-backslash"),   # xfce4
    # K("RC-Grave"): K("RC-Shift-backslash"),       # xfce4
    # In-App Tab switching
    # K("M-Tab"): K("C-Tab"),                       # Chromebook/IBM - In-App Tab switching
    # K("M-Shift-Tab"): K("C-Shift-Tab"),           # Chromebook/IBM - In-App Tab switching
    # K("M-Grave") : K("C-Shift-Tab"),              # Chromebook/IBM - In-App Tab switching
    K("Super-Tab"): K("LC-Tab"),                  # Default not-chromebook
    K("Super-Shift-Tab"): K("LC-Shift-Tab"),      # Default not-chromebook

    # Fn to Alt style remaps
    K("RM-Enter"): K("insert"),                   # Insert
    
    # emacs style
    K("Super-a"): K("Home"),                      # Beginning of Line
    K("Super-e"): K("End"),                       # End of Line
    K("Super-b"): K("Left"),
    K("Super-f"): K("Right"),
    K("Super-n"): K("Down"),
    K("Super-p"): K("Up"),
    K("Super-k"): [K("Shift-End"), K("Backspace")],
    K("Super-d"): K("Delete"),

    # K("M-RC-Space"): K(""),                   # Open Finder - Placeholder

    # Wordwise
    K("RC-Left"): K("Home"),                      # Beginning of Line
    K("RC-Shift-Left"): K("Shift-Home"),          # Select all to Beginning of Line
    K("RC-Right"): K("End"),                      # End of Line
    K("RC-Shift-Right"): K("Shift-End"),          # Select all to End of Line
    # K("RC-Left"): K("C-LEFT_BRACE"),              # Firefox-nw - Back
    # K("RC-Right"): K("C-RIGHT_BRACE"),            # Firefox-nw - Forward
    # K("RC-Left"): K("M-LEFT"),                    # Chrome-nw - Back
    # K("RC-Right"): K("M-RIGHT"),                  # Chrome-nw - Forward
    K("RC-Up"): K("C-Home"),                      # Beginning of File
    K("RC-Shift-Up"): K("C-Shift-Home"),          # Select all to Beginning of File
    K("RC-Down"): K("C-End"),                     # End of File
    K("RC-Shift-Down"): K("C-Shift-End"),         # Select all to End of File
    # K("RM-Backspace"): K("Delete"),               # Chromebook/IBM - Delete
    K("Super-Backspace"): K("C-Backspace"),       # Delete Left Word of Cursor
    K("Super-Delete"): K("C-Delete"),             # Delete Right Word of Cursor
    # K("LM-Backspace"): K("C-Backspace"),          # Chromebook/IBM - Delete Left Word of Cursor
    K("M-Backspace"): K("C-Backspace"),           # Default not-chromebook
    K("RC-Backspace"): K("C-Shift-Backspace"),    # Delete Entire Line Left of Cursor
    K("Alt-Delete"): K("C-Delete"),               # Delete Right Word of Cursor
    # K(""): pass_through_key,                      # cancel
    # K(""): K(""),                                 #
})

define_keymap(lambda wm_class: wm_class.casefold() not in mscodes,{
    # Wordwise remaining - for Everything but VS Code
    K("M-Left"): K("C-Left"),               # Left of Word
    K("M-Shift-Left"): K("C-Shift-Left"),   # Select Left of Word
    K("M-Right"): K("C-Right"),             # Right of Word
    K("M-Shift-Right"): K("C-Shift-Right"), # Select Right of Word
    K("M-Shift-g"): K("C-Shift-g"),         # View source control
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
    K("Super-Space"): K("LC-Space"),                        # Basic code completion
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
    # K("Super-c"): K("LC-c"),                    # Default - Terminal - Sigint
    # K("Super-x"): K("LC-x"),                    # Default - Terminal - Exit nano
    # K("M-c"): K("LC-c"),                        #  Chromebook/IBM - Terminal - Sigint
    # K("M-x"): K("LC-x"),                        #  Chromebook/IBM - Terminal - Exit nano
    # K("Super-C-g"): K("C-f2"),                  # Default - Sublime - find_all_under
    # K("C-M-g"): K("C-f2"),                      # Chromebook/IBM - Sublime - find_all_under
    # K("Super-Shift-up"): K("M-Shift-up"),       # multi-cursor up - Sublime
    # K("Super-Shift-down"): K("M-Shift-down"),   # multi-cursor down - Sublime
    # K(""): pass_through_key,                    # cancel
    # K(""): K(""),                               #
}, "Code")

# Keybindings for Sublime Text
define_keymap(re.compile("Sublime_text", re.IGNORECASE),{
    # K("Super-c"): K("LC-c"),                    # Default - Terminal - Sigint
    # K("Super-x"): K("LC-x"),                    # Default - Terminal - Exit nano
    # K("M-c"): K("LC-c"),                        #  Chromebook/IBM - Terminal - Sigint
    # K("M-x"): K("LC-x"),                        #  Chromebook/IBM - Terminal - Exit nano
    K("Super-Space"): K("C-Space"),             # Basic code completion
    K("C-Super-up"): K("M-o"),                  # Switch file
    K("Super-RC-f"): K("f11"),                  # toggle_full_screen
    K("C-M-v"): [K("C-k"), K("C-v")],           # paste_from_history
    K("C-up"): pass_through_key,                # cancel scroll_lines up
    K("C-M-up"): K("C-up"),                     # scroll_lines up
    K("C-down"): pass_through_key,              # cancel scroll_lines down
    K("C-M-down"): K("C-down"),                 # scroll_lines down
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
    # K("M-Refresh"): pass_through_key,           # Chromebook/IBM - cancel find_all_under
    # K("M-C-g"): K("M-Refresh"),                 # Chromebook/IBM - find_all_under
    K("Super-C-g"): K("M-f3"),                  # Default - find_all_under
    K("C-Shift-up"): pass_through_key,          # cancel swap_line_up
    K("Super-M-up"): K("C-Shift-up"),           # swap_line_up
    K("C-Shift-down"): pass_through_key,        # cancel swap_line_down
    K("Super-M-down"): K("C-Shift-down"),       # swap_line_down
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
    # K("LC-Right"):K("C-M-Right"),                 # Default SL - Change workspace (budgie)
    # K("LC-Left"):K("C-M-Left"),                   # Default SL - Change workspace (budgie)
    # K("LC-Left"):K("C-M-End"),                    # SL - Change workspace xfce4     
    # K("LC-Left"):K("Super-Left"),                 # SL - Change workspace eos 
    # K("LC-Right"):K("C-M-Home"),                  # SL - Change workspace xfce4     
    # K("LC-Right"):K("Super-Right"),               # SL - Change workspace eos
    # K("LC-Right"):K("Super-Page_Up"),             # SL - Change workspace (ubuntu/fedora)
    # K("LC-Left"):K("Super-Page_Down"),            # SL - Change workspace (ubuntu/fedora)
    # K("LC-Right"):K("Super-C-Up"),                # SL - Change workspace (popos)
    # K("LC-Left"):K("Super-C-Down"),               # SL - Change workspace (popos)
    # Ctrl Tab - In App Tab Switching
    K("LC-Tab") : K("LC-PAGE_DOWN"),
    K("LC-Shift-Tab") : K("LC-PAGE_UP"),
    K("LC-Grave") : K("LC-PAGE_UP"),
    # K("M-Tab"): pass_through_key,                 # Default not-xfce4 - Cmd Tab - App Switching Default
    # K("RC-Tab"): K("M-Tab"),                      # Default not-xfce4 - Cmd Tab - App Switching Default
    # K("RC-Shift-Tab"): K("M-Shift-Tab"),          # Default not-xfce4 - Cmd Tab - App Switching Default
    # Cmd Tab - App Switching Default
    # K("RC-Tab"): K("RC-backslash"),               # xfce4
    # K("RC-Shift-Tab"): K("RC-Shift-backslash"),   # xfce4
    # K("RC-Grave"): K("RC-Shift-backslash"),       # xfce4
    # Converts Cmd to use Ctrl-Shift
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
