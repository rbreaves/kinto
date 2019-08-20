# pip3 install pynput
# pip3 install --no-deps pynput

from pynput.keyboard import Key, Listener
import sys, subprocess

uitype=sys.argv[1]
apply_rules=sys.argv[2]
windows=sys.argv[3]
chromebook=sys.argv[4]
mac=sys.argv[5]

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

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

def is_ctrl_winchrome(key):
    if key == Key.ctrl:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to physical Alt key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Alt is now Ctrl')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Alt key.'.format(key))
        return False

def is_ctrl_mac(key):
    if key == Key.ctrl:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to physical Alt key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Command is now Ctrl')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Command key.'.format(key))
        return False

def is_ctrl_terminal(key):
    if key == Key.ctrl:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to physical Ctrl key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Ctrl remains Ctrl,\nwhile in terminal apps.')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Ctrl key.'.format(key))
        return False

def is_alt_chromebook(key):
    if key == Key.alt:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to the physical Ctrl key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Ctrl is now Alt')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Ctrl key.'.format(key))
        return False

def is_alt_windows(key):
    if key == Key.alt:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to the physical Ctrl key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Win/Super is now Alt')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Win/Super key.'.format(key))
        return False

def is_alt_mac(key):
    if key == Key.alt:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to the physical Ctrl key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Alt remains Alt')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Alt key.'.format(key))
        return False

def is_alt_chromebook_terminal(key):
    if key == Key.alt:
        # print(str(key).replace("Key.", "").title() +' successfully mapped to the physical Search key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Search is now Alt,\nwhile in terminals apps.')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Search key.'.format(key))
        return False

def is_super_winmac(key):
    if key == Key.cmd:
        # print('Super/Win successfully mapped to the physical Search key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Ctrl key is Super/Win')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Ctrl key.'.format(key))
        return False

def is_super_chromebook(key):
    if key == Key.cmd:
        # print('Super/Win successfully mapped to the physical Search key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Search key is Super/Win')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Search key.'.format(key))
        return False

def is_super_terminal(key):
    if key == Key.cmd:
        # print('Super/Win successfully mapped to the physical Alt key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Alt is now Super/Win,\nwhile in terminal apps.')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Alt key.'.format(key))
        return False

def is_super_mac_terminal(key):
    if key == Key.cmd:
        # print('Super/Win successfully mapped to the physical Alt key.'.format(key))
        print(color.GREEN + 'Success' + color.END + ' Command is now Super/Win,\nwhile in terminal apps.')
        return False
    elif key == Key.esc:
    	return False
    else:
        print('keymap failure, ' + str(key).replace("Key.", "").title() + ' may have been mapped to the physical Command key.'.format(key))
        return False

def chromebook_keys_gui():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm the new keymapping to Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_winchrome) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm the new keymapping to Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_chromebook) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Search" + color.END + " key to confirm the new keymapping to Super/Win..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_chromebook) as listener:
            listener.join()

def chromebook_keys_terminal():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm the new keymapping to Super/Win..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_terminal) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm the new keymapping to Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_terminal) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Search" + color.END + " key to confirm the new keymapping to Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_chromebook_terminal) as listener:
            listener.join()

def windows_keys_gui():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm the new keymapping to Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_winchrome) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Win/Super" + color.END + " key to confirm the new keymapping to Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_windows) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm the new keymapping to Win/Super..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_winmac) as listener:
            listener.join()

def windows_keys_terminal():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm the new keymapping to Super/Win..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_terminal) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Win/Super" + color.END + " key to confirm the new keymapping to Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_windows) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm the new keymapping to Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_terminal) as listener:
            listener.join()

def mac_keys_gui():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Command" + color.END + " key to confirm the new keymapping to Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_mac) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm it remains Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_mac) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm the new keymapping to Win/Super..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_winmac) as listener:
            listener.join()

def mac_keys_terminal():
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Command" + color.END + " key to confirm the new keymapping to Super/Win..")
    with Listener(
        # on_press=on_press,
        on_release=is_super_mac_terminal) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Alt" + color.END + " key to confirm it remains Alt..")
    with Listener(
        # on_press=on_press,
        on_release=is_alt_mac) as listener:
            listener.join()
    print()
    print(color.UNDERLINE + color.YELLOW + "Press the physical Ctrl" + color.END + " key to confirm it remains Ctrl..")
    with Listener(
        # on_press=on_press,
        on_release=is_ctrl_terminal) as listener:
            listener.join()

if uitype == 'gui':
    if chromebook == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.chromebook.gui $DISPLAY', shell=True).decode('utf-8')
        print()
        print("Testing chromebook - GUI apps - Kinto keymapping...")
        chromebook_keys_gui()

    if windows == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY', shell=True).decode('utf-8')
        print()
        print ("Testing windows keyboard - GUI apps - Kinto keymapping...")
        windows_keys_gui()

    if mac == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;xkbcomp -w0 -I$HOME/.xkb ~/.xkb/keymap/kbd.mac.gui $DISPLAY', shell=True).decode('utf-8')
        print ("Testing mac keyboard - GUI apps - Kinto keymapping...")
        mac_keys_gui()

if uitype == 'term':
    if chromebook == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;setxkbmap -option altwin:swap_lalt_lwin', shell=True).decode('utf-8')
        print("Testing chromebook - terminal - Kinto keymapping...")
        chromebook_keys_terminal()

    if windows == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;setxkbmap -option altwin:swap_alt_win', shell=True).decode('utf-8')
        print ("Testing windows keyboard - terminal - Kinto keymapping...")
        windows_keys_terminal()

    if mac == '1':
        if apply_rules == '1':
            subprocess.check_output('setxkbmap -option;setxkbmap -option altwin:swap_alt_win', shell=True).decode('utf-8')
        print ("Testing mac keyboard - terminal - Kinto keymapping...")
        mac_keys_terminal()
        
if apply_rules == '1':
    subprocess.run('setxkbmap -option', shell=True)