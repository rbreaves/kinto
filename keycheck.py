#!/usr/bin/env python3

# pip3 install pynput
# pip3 install --no-deps pynput

from pynput.keyboard import Key, Listener
import sys, subprocess, time
delay=3

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def countdown(secs):
    for i in range(0,secs):
        print(secs-i, end="\r", flush=True)
        time.sleep(1)

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values

modifier_keys = {
    "primary":"",
    "secondary":"",
    "rprimary":"",
    "rsecondary":"",
    "capslock":"",
    "capswap":""
}

def set_key(key):
    global modifiery_keys
    print("\nWhich key would you like to set?\n")

    while True:
        try:
            keytype = int(input(
                "1) Ctrl\n" +
                "2) Alt\n" +
                "3) Super/Win/Cmd/Chrome search key\n"))
            if keytype < 4 and keytype > 0:
                break
        except:
            print("That's not a valid option!")
    print("")
    if keytype == 1:
        modifier_keys[key] = "Ctrl"
    elif keytype == 2:
        modifier_keys[key] = "Alt"
    elif keytype == 3:
        modifier_keys[key] = "Cmd"

def set_cap():
    global modifiery_keys
    print("\nWhich key would you like to swap?\n")

    while True:
        try:
            keytype = int(input(
                "1) Ctrl (swap)\n" +
                "2) Ctrl (duplicate)\n" +
                "3) Esc (swap)\n"))
            if keytype < 4 and keytype > 0:
                break
        except:
            print("That's not a valid option!")
    print("")
    if keytype == 1:
        modifier_keys["capslock"] = "Ctrl-swap"
    elif keytype == 2:
        modifier_keys["capslock"] = "Ctrl-dup"
    elif keytype == 3:
        modifier_keys["capswap"] = "Esc"

def is_primary(key):
    global modifiery_keys
    if not (str(key).replace("Key.", "").title() == "Enter" or str(key).replace("Key.", "").title() == "Esc"):
        print(str(key).replace("Key.", "").title() + " will be remapped to Ctrl, the Cmd ⌘  key position.")
        # countdown(3)
        modifier_keys["primary"] = str(key).replace("Key.", "").title()
        return False
    elif str(key).replace("Key.", "").title() == "Esc":
        modifier_keys["primary"] = "Esc"
        # countdown(3)
        return False
    else:
        return True

def is_secondary(key):
    global modifiery_keys
    if not (str(key).replace("Key.", "").title() == "Enter" or str(key).replace("Key.", "").title() == "Esc"):
        print(str(key).replace("Key.", "").title() + " will be remapped to Alt, the Option ⌥  key position.")
        # countdown(3)
        modifier_keys["secondary"] = str(key).replace("Key.", "").title()
        return False
    elif str(key).replace("Key.", "").title() == "Esc":
        modifier_keys["secondary"] = "Esc"
        # countdown(3)
        return False
    else:
        return True

def is_rprimary(key):
    global modifiery_keys
    if not (str(key).replace("Key.", "").title() == "Enter" or str(key).replace("Key.", "").title() == "Esc"):
        print(str(key).replace("Key.", "").title() + " will be remapped to Ctrl, the Cmd ⌘  key position.")
        # countdown(3)
        modifier_keys["rprimary"] = str(key).replace("Key.", "").title()
        return False
    elif str(key).replace("Key.", "").title() == "Esc":
        modifier_keys["rprimary"] = "Esc"
        # countdown(3)
        return False
    else:
        return True

def is_rsecondary(key):
    global modifiery_keys
    if not (str(key).replace("Key.", "").title() == "Enter" or str(key).replace("Key.", "").title() == "Esc"):
        print(str(key).replace("Key.", "").title() + " will be remapped to Alt, the Option ⌥  key position.")
        # countdown(3)
        modifier_keys["rsecondary"] = str(key).replace("Key.", "").title()
        return False
    elif str(key).replace("Key.", "").title() == "Esc":
        modifier_keys["rsecondary"] = "Esc"
        # countdown(3)
        return False
    else:
        return True


print(color.UNDERLINE + color.YELLOW + "\n\nPlease ignore the FN key." + color.END + " FN cannot be remapped by software, some Thinkpads can swap it with Ctrl in the BIOS.\n")
input("Press Enter to continue...\n\n")
print(chr(27) + "[2J")

while True:
    global modifiery_keys
    
    
    print(color.UNDERLINE + color.YELLOW + "\n\nPress the 1st key Left of the spacebar" + color.END + " (Press Esc to set manaully)\n")
    print("    👇 \n")
    print(" □ □ ▣ ░░░░░░░\n")
    with Listener(
        on_release=is_primary,suppress=True) as listener:
            try:
                listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))

    if modifier_keys["primary"] != "Esc":
        choice = yn_choice("Is this correct?")
        if(choice):
            print("Left Physical " + modifier_keys["primary"] + " = Ctrl/Cmd ⌘")
            # listener.stop()
            break
    else:
        set_key("primary")
        print("Left Physical " + modifier_keys["primary"] + " = Ctrl/Cmd ⌘\n")
        # listener.stop()
        input("Press Enter to continue...\n\n")
        break

print(chr(27) + "[2J")

print(listener)

while True:
    global modifiery_keys
    print(color.UNDERLINE + color.YELLOW + "\n\nPress the 2nd key Left of the spacebar" + color.END + " (Press Esc to set manaully)\n")
    print("  👇\n")
    print(" □ ▣ □ ░░░░░░░\n")
    
    with Listener(
        on_release=is_secondary,suppress=True) as listener:
            try:
                listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))

    if modifier_keys["secondary"] != "Esc":
        choice = yn_choice("Is this correct?")
        if(choice):
            # listener.stop()
            # print("Left Physical " + modifier_keys["secondary"] + " = Alt/Option ⌥")
            break
    else:
        set_key("secondary")
        print("Left Physical " + modifier_keys["secondary"] + " = Alt/Option ⌥\n")
        # listener.stop()
        input("Press Enter to continue...\n\n")
        break

print(chr(27) + "[2J")

while True:
    global modifiery_keys
    print(color.UNDERLINE + color.YELLOW + "\n\nPress the 1st key Right of the spacebar" + color.END + " (Press Esc to set manaully)\n")
    print("        👇 \n")
    print(" ░░░░░░░ ▣ □ \n")
    
    with Listener(
        on_release=is_rprimary,suppress=True) as listener:
            try:
                listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))

    if modifier_keys["rprimary"] != "Esc":
        choice = yn_choice("Is this correct?")
        if(choice):
            # listener.stop()
            # print("Right Physical " + modifier_keys["rprimary"] + " = Ctrl/Cmd ⌘")
            break
    else:
        set_key("rprimary")
        print("Right Physical " + modifier_keys["rprimary"] + " = Ctrl/Cmd ⌘\n")
        # listener.stop()
        input("Press Enter to continue...\n\n")
        break

print(chr(27) + "[2J")

while True:
    print(color.UNDERLINE + color.YELLOW + "\n\nPress the 2nd key Right of the spacebar" + color.END + " (Press Esc to set manaully)\n")
    print("          👇\n")
    print(" ░░░░░░░ □ ▣ \n")
    

    
    with Listener(
        on_release=is_rsecondary,suppress=True) as listener:
            try:
                listener.join()
            except MyException as e:
                print('{0} was pressed'.format(e.args[0]))

    if modifier_keys["rsecondary"] != "Esc":
        choice = yn_choice("Is this correct?")
        if(choice):
            # listener.stop()
            # print("Right Physical " + modifier_keys["rsecondary"] + " = Alt/Option ⌥")
            break
    else:
        set_key("rsecondary")
        print("Right Physical " + modifier_keys["rsecondary"] + " = Alt/Option ⌥\n")
        # listener.stop()
        input("Press Enter to continue...\n\n")
        break

print(chr(27) + "[2J")

if modifier_keys["secondary"] != "Ctrl":
    print(color.UNDERLINE + color.YELLOW + "GUI Usage (Physical Ctrl key)\n"+ color.END)
    print("Ctrl key will be mapped to Super. (Search key on chromebooks)\n")
    print("👇\n")
    print(" ▣ □ □ ░░░░░░░\n")

    print("Note: Super may still activate Ctrl based shortcuts\n")
    print("at times depending on application or system level shortcut.\n")
    print("This will only be done to align shortcuts to their expected functionality.\n")

    input("Press Enter to continue...\n\n")
    # print(chr(27) + "[2J")

    print(color.UNDERLINE + color.YELLOW + "Terminal Usage" + color.END + "\n")
    print("Ctrl key will be the Ctrl key.\n")
    print("👇\n")
    print(" ▣ □ □ ░░░░░░░\n\n")
    print("The Cmd ⌘  key position during terminal usage will usually be Ctrl+Shift.\n")
    print("    👇 \n")
    print(" □ □ ▣ ░░░░░░░\n\n")
    input("Press Enter to continue...\n\n")
else:
    print("Chromebook detected.")

    print(color.UNDERLINE + color.YELLOW + "Terminal Usage" + color.END + "\n")
    print(" □ capslock/search key = Alt\n")
    print(" shift\n")
    print(" ▣ □ ░░░░░░░")
    print("☝️\n")

    input("Press Enter to continue...\n\n")

print(chr(27) + "[2J")

choice = yn_choice(color.UNDERLINE + color.YELLOW + "Do you want to swap Capslock with another key?" + color.END + "\n","n")
if(choice):
    set_cap()