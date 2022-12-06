from keyszer.config_api import *

# Can be removed after keyszer release v0.7 or later:
from keyszer.config_api import to_US_keystrokes, unicode_keystrokes, Trigger

# Needed for showing GUI notifications
from subprocess import run



############################################################################
###                                                                      ###
###                                                                      ###
###       ██████  ██████  ████████ ███████ ██████  ███████  ██████       ###
###      ██    ██ ██   ██    ██    ██      ██   ██ ██      ██            ###
###      ██    ██ ██████     ██    ███████ ██████  █████   ██            ###
###      ██    ██ ██         ██         ██ ██      ██      ██            ###
###       ██████  ██         ██    ███████ ██      ███████  ██████       ###
###                                                                      ###
###                                                                      ###
############################################################################

###########   START OF OPTION KEY SPECIAL CHARACTER ENTRY SCHEME    #############
#################################################################################
### Full list of special characters on Apple US and ABC Extended keyboard layouts: 
### https://github.org/RedBearAK/optspecialchars

# Variables to enable either Option Key Special Character entry scheme by default
# (ENABLE ONLY ONE, NOT BOTH! Layouts must be exclusive.)
_optspec_US = True              # Default: True
_optspec_ABC = False            # Default: False

# Short names for the string and Unicode processing helper functions
ST = to_US_keystrokes
UC = unicode_keystrokes


def check_optspec_exclusive():
    """Check to make sure that both Option-key layout variables aren't enabled at the same time."""
    # Needs "from subprocess import run" somewhere
    if _optspec_ABC and _optspec_US:
        run('notify-send -u critical ERROR "Don\'t enable both Option-key Special Character Entry\
            \rlayouts at the same time."', shell=True)
        raise ValueError(f'\n\nDon\'t set both "_optspec_ABC" and "_optspec_US" layout variables to True at the same time.\n')


# Make sure only one Option-key layout is enabled (or none)
check_optspec_exclusive()


def toggle_optspec_US():
    """Toggle the value of the _optspecialchars_US variable"""
    # Needs "from subprocess import run" somewhere
    def _toggle_optspec_US():
        global _optspec_US
        global _optspec_ABC
        if _optspec_ABC:
            _optspec_ABC = False                        # Disable the other layout, if active
        _optspec_US = not _optspec_US
        if _optspec_US:
            run('notify-send -u critical ALERT "Kinto OptSpecialChars-US is now ENABLED.\
                \rWill interfere with Alt & Shift+Alt shortcuts!\
                \rDisable with Shift+Opt+Cmd+U."', shell=True)
            print("(DD) OptSpecialChars-US is now ENABLED.", flush=True)
        else:
            run('notify-send -u critical ALERT "Kinto OptSpecialChars-US is now DISABLED.\
                \rRe-enable with Shift+Opt+Cmd+U"', shell=True)
            print("(DD) OptSpecialChars-US is now DISABLED.", flush=True)

    return _toggle_optspec_US


def toggle_optspec_ABC():
    """Toggle the value of the _optspecialchars_ABC variable"""
    # Needs "from subprocess import run" somewhere
    def _toggle_optspec_ABC():
        global _optspec_ABC
        global _optspec_US
        if _optspec_US:
            _optspec_US = False                         # Disable the other layout, if active
        _optspec_ABC = not _optspec_ABC
        if _optspec_ABC:
            run('notify-send -u critical ALERT "Kinto OptSpecialChars-ABC is now ENABLED.\
                \rWill interfere with Alt & Shift+Alt shortcuts!\
                \rDisable with Shift+Opt+Cmd+X."', shell=True)
            print("(DD) OptSpecialChars-ABC is now ENABLED.", flush=True)
        else:
            run('notify-send -u critical ALERT "Kinto OptSpecialChars-ABC is now DISABLED.\
                \rRe-enable with Shift+Opt+Cmd+X."', shell=True)
            print("(DD) OptSpecialChars-ABC is now DISABLED.", flush=True)

    return _toggle_optspec_ABC


def disable_optspec():
    """Disable both Option key special character entry scheme layouts"""
    # Needs "from subprocess import run" somewhere
    def _disable_optspec():
        global _optspec_ABC
        global _optspec_US
        _optspec_ABC = False
        _optspec_US = False
        run('notify-send -u critical ALERT "Kinto OptSpecialChars (US/ABC) is now DISABLED.\
            \rTo re-enable ABC Extended: Shift+Opt+Cmd+X\
            \rTo re-enable Standard US: Shift+Opt+Cmd+U"', shell=True)
        print("(DD) OptSpecialChars (US/ABC) is now DISABLED.", flush=True)

    return _disable_optspec


keymap("OptSpecialChars toggles", {
    C("Shift-Alt-RC-o"):        disable_optspec(),      # Disable all layouts
    C("Shift-Alt-RC-u"):        toggle_optspec_US(),    # Toggle the US layout
    C("Shift-Alt-RC-x"):        toggle_optspec_ABC(),   # Toggle the ABC Extended layout
}, when = lambda ctx: ctx.wm_class.casefold() not in terminals)


################################################################
# Set this variable to False to disable the alert that appears 
# when using Apple logo shortcut (Shift+Option+K)
_applelogoalert = True


def apple_logo_alert():
    """Show a notification about needing Baskerville Old Face font for displaying Apple logo"""
    # Needs "from subprocess import run" somewhere
    def _apple_logo_alert():
        global _applelogoalert
        if _applelogoalert:
            run('notify-send -u critical ALERT "Apple logo requires Baskerville Old Face font.\
                \rTo disable warning, change \\"_applelogoalert\\" \
                \rvariable value in config file to \\"False\\"."', shell=True)

    return _apple_logo_alert



######################################################################################
###                                                                                ###
###                                                                                ###
###      ██████  ███████  █████  ██████      ██   ██ ███████ ██    ██ ███████      ###
###      ██   ██ ██      ██   ██ ██   ██     ██  ██  ██       ██  ██  ██           ###
###      ██   ██ █████   ███████ ██   ██     █████   █████     ████   ███████      ###
###      ██   ██ ██      ██   ██ ██   ██     ██  ██  ██         ██         ██      ###
###      ██████  ███████ ██   ██ ██████      ██   ██ ███████    ██    ███████      ###
###                                                                                ###
###                                                                                ###
######################################################################################

# variables to store dead keys diacritic accent character Unicode address
ac_Chr = None
_ac_Chr = None


def set_dead_key_char(hex_unicode_addr):
    """Set the value of the dead keys accent character variable, and its alternate."""
    def fn():
        global ac_Chr
        global _ac_Chr
        if hex_unicode_addr is None or hex_unicode_addr == 0x0000:
            pass
        else:
            _ac_Chr = hex_unicode_addr
        ac_Chr = hex_unicode_addr

    return fn


def get_dead_key_char():
    """Get the value of the alternate dead key accent character 
        variable, and print/type the resulting Unicode character."""
    def fn():
        global _ac_Chr
        return UC(_ac_Chr)

    return fn


setDK = set_dead_key_char
getDK = get_dead_key_char

deadkeys_ABC = [
    # Dead keys on ABC Extended keyboard layout (25, plus substitutes for problematic chars)
    0x0060,                     # Dead Keys Accent: Grave
    0x02C6,                     # Dead Keys Accent: Circumflex
    0x02D9,                     # Dead Keys Accent: Dot Above
    0x00B4,                     # Dead Keys Accent: Acute
    ###  Combining Double Grave has issues (spacing behavior) - substituting {U+02F5}
    0x030F,                     # Dead Keys Accent: Combining Double Grave
    ###  Substitute for Double Grave: Modifier Letter Middle Double Grave Accent
    0x02F5,                     # Dead Keys Accent: Double Grave - substitute for {U+030F}
    0x00A8,                     # Dead Keys Accent: Umlaut
    0x02BC,                     # Dead Keys Accent: Apostrophe/Horn
    0x002C,                     # Dead Keys Accent: Comma Below
    0x00AF,                     # Dead Keys Accent: Macron/Line Above
    ###  Combining Inverted Breve has issues (spacing behavior) - substituting {U+1D16}
    0x0311,                     # Dead Keys Accent: Combining Inverted Breve
    ###  Substitute for Inverted Breve: Latin Small Letter Top Half O
    0x1D16,                     # Dead Keys Accent: Inverted Breve - substitute for {U+0311}
    ###  Combining Tilde Below has issues (spacing behavior) - substituting {U+02F7}
    0x0330,                     # Dead Keys Accent: Combining Tilde Below
    ###  Substitute for Tilde Below: Modifier Letter Low Tilde
    0x02F7,                     # Dead Keys Accent: Tilde Below
    0x2038,                     # Dead Keys Accent: Caret/Circumflex Below
    0x02CD,                     # Dead Keys Accent: Low Macron/Line Below
    0x02DD,                     # Dead Keys Accent: Double Acute
    0x02DA,                     # Dead Keys Accent: Ring Above
    0x002D,                     # Dead Keys Accent: Stroke/Hyphen-Minus
    0x2116,                     # Dead Keys Accent: Numero Sign
    0x02C0,                     # Dead Keys Accent: Hook Above/Glottal Stop
    0x002E,                     # Dead Keys Accent: Dot Below
    0x00B8,                     # Dead Keys Accent: Cedilla/Cedille
    0x02C7,                     # Dead Keys Accent: Caron/hacek
    0x02D8,                     # Dead Keys Accent: Breve
    0x02DC,                     # Dead Keys Accent: Tilde
    0x02DB,                     # Dead Keys Accent: Ogonek
    0x0294,                     # Dead Keys Accent: Hook
]

deadkeys_US = [
    # Dead keys on standard US keyboard layout (5)
    0x0060,                     # Dead Keys Accent: Grave
    0x00B4,                     # Dead Keys Accent: Acute
    0x00A8,                     # Dead Keys Accent: Umlaut
    0x02C6,                     # Dead Keys Accent: Circumflex
    0x02DC,                     # Dead Keys Accent: Tilde
]

# Join the two dead keys lists together
deadkeys_list = []
deadkeys_list.extend(deadkeys_ABC)
deadkeys_list.extend(deadkeys_US)


#####################################
###   DEAD KEYS KEYMAPS - START   ###
#####################################
# Dead Keys conditional keymaps
# only active when the dead key variable matches
# and the appropriate layout variable (US or ABC) is True

#################################################
###  DEAD KEYS KEYMAPS - ABC EXTENDED LAYOUT  ###
#################################################

keymap("DK-ABC - Grave", {
    # Option+Grave              {U+0060}
    # Valid keys:
    # a e i n o u v w y
    # A E I N O U V W Y
    C("A"):                     UC(0x00E0),                     # à Latin Small Letter A with Grave
    C("E"):                     UC(0x00E8),                     # è Latin Small Letter E with Grave
    C("I"):                     UC(0x00EC),                     # ì Latin Small Letter I with Grave
    C("N"):                     UC(0x01F9),                     # ǹ Latin Small Letter N with Grave
    C("O"):                     UC(0x00F2),                     # ò Latin Small Letter O with Grave
    C("U"):                     UC(0x00F9),                     # ù Latin Small Letter U with Grave
    C("V"):                     UC(0x01DC),                     # ǜ Latin Small Letter U w/Diaeresis and Grave
    C("W"):                     UC(0x1E81),                     # ẁ Latin Small Letter W with Grave
    C("Y"):                     UC(0x1EF3),                     # ỳ Latin Small Letter Y with Grave
    C("Shift-A"):               UC(0x00C0),                     # À Latin Capital Letter A with Grave
    C("Shift-E"):               UC(0x00C8),                     # È Latin Capital Letter E with Grave
    C("Shift-I"):               UC(0x00CC),                     # Ì Latin Capital Letter I with Grave
    C("Shift-N"):               UC(0x01F8),                     # Ǹ Latin Capital Letter N with Grave
    C("Shift-O"):               UC(0x00D2),                     # Ò Latin Capital Letter O with Grave
    C("Shift-U"):               UC(0x00D9),                     # Ù Latin Capital Letter U with Grave
    C("Shift-V"):               UC(0x01DB),                     # Ǜ Latin Capital Letter U w/Diaeresis and Grave
    C("Shift-W"):               UC(0x1E80),                     # Ẁ Latin Capital Letter W with Grave
    C("Shift-Y"):               UC(0x1EF2),                     # Ỳ Latin Capital Letter Y with Grave
}, when = lambda _: ac_Chr == 0x0060 and _optspec_ABC is True)

keymap("DK-ABC - Circumflex", {
    # Option+6                  {U+02C6}
    # Valid keys:
    # a c e g h i j m n o s u w y z
    # A C E G H I J M N O S U W Y Z
    C("A"):                     UC(0x00E2),                     # â Latin Small Letter A with Circumflex
    C("C"):                     UC(0x0109),                     # ĉ Latin Small Letter C with Circumflex
    C("E"):                     UC(0x00EA),                     # ê Latin Small Letter E with Circumflex
    C("G"):                     UC(0x011D),                     # ĝ Latin Small Letter G with Circumflex
    C("H"):                     UC(0x0125),                     # ĥ Latin Small Letter H with Circumflex
    C("I"):                     UC(0x00EE),                     # î Latin Small Letter I with Circumflex
    C("J"):                     UC(0x0135),                     # ĵ Latin Small Letter J with Circumflex
    C("M"):                     [UC(0x006D),UC(0x0302)],        # m̂ Latin Small Letter M with Circumflex
    C("N"):                     [UC(0x006E),UC(0x0302)],        # n̂ Latin Small Letter N with Circumflex
    C("O"):                     UC(0x00F4),                     # ô Latin Small Letter O with Circumflex
    C("S"):                     UC(0x015D),                     # ŝ Latin Small Letter S with Circumflex
    C("U"):                     UC(0x00FB),                     # û Latin Small Letter U with Circumflex
    C("W"):                     UC(0x0175),                     # ŵ Latin Small Letter W with Circumflex
    C("Y"):                     UC(0x0177),                     # ŷ Latin Small Letter Y with Circumflex
    C("Z"):                     UC(0x1E91),                     # ẑ Latin Small Letter Z with Circumflex
    C("Shift-A"):               UC(0x00C2),                     # Â Latin Capital Letter A with Circumflex
    C("Shift-C"):               UC(0x0108),                     # Ĉ Latin Capital Letter C with Circumflex
    C("Shift-E"):               UC(0x00CA),                     # Ê Latin Capital Letter E with Circumflex
    C("Shift-G"):               UC(0x011C),                     # Ĝ Latin Capital Letter G with Circumflex
    C("Shift-H"):               UC(0x0124),                     # Ĥ Latin Capital Letter H with Circumflex
    C("Shift-I"):               UC(0x00CE),                     # Î Latin Capital Letter I with Circumflex
    C("Shift-J"):               UC(0x0134),                     # Ĵ Latin Capital Letter J with Circumflex
    C("Shift-M"):               [UC(0x004D),UC(0x0302)],        # M̂ Latin Capital Letter M with Circumflex
    C("Shift-N"):               [UC(0x004E),UC(0x0302)],        # N̂ Latin Capital Letter N with Circumflex
    C("Shift-O"):               UC(0x00D4),                     # Ô Latin Capital Letter O with Circumflex
    C("Shift-S"):               UC(0x015C),                     # Ŝ Latin Capital Letter S with Circumflex
    C("Shift-U"):               UC(0x00DB),                     # Û Latin Capital Letter U with Circumflex
    C("Shift-W"):               UC(0x0174),                     # Ŵ Latin Capital Letter W with Circumflex
    C("Shift-Y"):               UC(0x0176),                     # Ŷ Latin Capital Letter Y with Circumflex
    C("Shift-Z"):               UC(0x1E90),                     # Ẑ Latin Capital Letter Z with Circumflex
}, when = lambda _: ac_Chr == 0x02C6 and _optspec_ABC is True)

keymap("DK-ABC - Dot Above", {
    # Option+W                  {U+02D9}
    # Valid keys:
    # a b c d e f g h i m n o p r s t w x y z
    # A B C D E F G H I M N O P R S T W X Y Z
    C("A"):                     UC(0x0227),                     # ȧ Latin Small Letter A with Dot Above
    C("B"):                     UC(0x1E03),                     # ḃ Latin Small Letter B with Dot Above
    C("C"):                     UC(0x010B),                     # ċ Latin Small Letter C with Dot Above
    C("D"):                     UC(0x1E0B),                     # ḋ Latin Small Letter D with Dot Above
    C("E"):                     UC(0x0117),                     # ė Latin Small Letter E with Dot Above
    C("F"):                     UC(0x1E1F),                     # ḟ Latin Small Letter F with Dot Above
    C("G"):                     UC(0x0121),                     # ġ Latin Small Letter G with Dot Above
    C("H"):                     UC(0x1E23),                     # ḣ Latin Small Letter H with Dot Above
    C("I"):                     UC(0x0131),                     # ı Latin Small Letter Dotless I
    C("M"):                     UC(0x1E41),                     # ṁ Latin Small Letter M with Dot Above
    C("N"):                     UC(0x1E45),                     # ṅ Latin Small Letter N with Dot Above
    C("O"):                     UC(0x022F),                     # ȯ Latin Small Letter O with Dot Above
    C("P"):                     UC(0x1E57),                     # ṗ Latin Small Letter P with Dot Above
    C("R"):                     UC(0x1E59),                     # ṙ Latin Small Letter R with Dot Above
    C("S"):                     UC(0x1E61),                     # ṡ Latin Small Letter S with Dot Above
    C("T"):                     UC(0x1E6B),                     # ṫ Latin Small Letter T with Dot Above
    C("W"):                     UC(0x1E87),                     # ẇ Latin Small Letter W with Dot Above
    C("X"):                     UC(0x1E8B),                     # ẋ Latin Small Letter X with Dot Above
    C("Y"):                     UC(0x1E8F),                     # ẏ Latin Small Letter Y with Dot Above
    C("Z"):                     UC(0x017C),                     # ż Latin Small Letter Z with Dot Above
    C("Shift-A"):               UC(0x0226),                     # Ȧ Latin Capital Letter A with Dot Above
    C("Shift-B"):               UC(0x1E02),                     # Ḃ Latin Capital Letter B with Dot Above
    C("Shift-C"):               UC(0x010A),                     # Ċ Latin Capital Letter C with Dot Above
    C("Shift-D"):               UC(0x1E0A),                     # Ḋ Latin Capital Letter D with Dot Above
    C("Shift-E"):               UC(0x0116),                     # Ė Latin Capital Letter E with Dot Above
    C("Shift-F"):               UC(0x1E1E),                     # Ḟ Latin Capital Letter F with Dot Above
    C("Shift-G"):               UC(0x0120),                     # Ġ Latin Capital Letter G with Dot Above
    C("Shift-H"):               UC(0x1E22),                     # Ḣ Latin Capital Letter H with Dot Above
    C("Shift-I"):               UC(0x0130),                     # İ Latin Capital Letter I with Dot Above
    C("Shift-M"):               UC(0x1E40),                     # Ṁ Latin Capital Letter M with Dot Above
    C("Shift-N"):               UC(0x1E44),                     # Ṅ Latin Capital Letter N with Dot Above
    C("Shift-O"):               UC(0x022E),                     # Ȯ Latin Capital Letter O with Dot Above
    C("Shift-P"):               UC(0x1E56),                     # Ṗ Latin Capital Letter P with Dot Above
    C("Shift-R"):               UC(0x1E58),                     # Ṙ Latin Capital Letter R with Dot Above
    C("Shift-S"):               UC(0x1E60),                     # Ṡ Latin Capital Letter S with Dot Above
    C("Shift-T"):               UC(0x1E6A),                     # Ṫ Latin Capital Letter T with Dot Above
    C("Shift-W"):               UC(0x1E86),                     # Ẇ Latin Capital Letter W with Dot Above
    C("Shift-X"):               UC(0x1E8A),                     # Ẋ Latin Capital Letter X with Dot Above
    C("Shift-Y"):               UC(0x1E8E),                     # Ẏ Latin Capital Letter Y with Dot Above
    C("Shift-Z"):               UC(0x017B),                     # Ż Latin Capital Letter Z with Dot Above
}, when = lambda _: ac_Chr == 0x02D9 and _optspec_ABC is True)

keymap("DK-ABC - Acute", {
    # Option+E                  {U+00B4}
    # Valid keys:
    # a c e g i m n o p r s w y z
    # A C E G I M N O P R S W Y Z
    C("A"):                     UC(0x00E1),                     # á Latin Small Letter A with Acute
    C("C"):                     UC(0x0107),                     # ć Latin Small Letter C with Acute
    C("E"):                     UC(0x00E9),                     # é Latin Small Letter E with Acute
    C("G"):                     UC(0x01F5),                     # ǵ Latin Small Letter G with Acute
    C("I"):                     UC(0x00ED),                     # í Latin Small Letter I with Acute
    C("M"):                     UC(0x1E3F),                     # ḿ Latin Small Letter M with Acute
    C("N"):                     UC(0x0144),                     # ń Latin Small Letter N with Acute
    C("O"):                     UC(0x00F3),                     # ó Latin Small Letter O with Acute
    C("P"):                     UC(0x1E55),                     # ṕ Latin Small Letter P with Acute
    C("R"):                     UC(0x0155),                     # ŕ Latin Small Letter R with Acute
    C("S"):                     UC(0x015B),                     # ś Latin Small Letter S with Acute
    C("W"):                     UC(0x1E83),                     # ẃ Latin Small Letter W with Acute
    C("Y"):                     UC(0x00FD),                     # ý Latin Small Letter Y with Acute
    C("Z"):                     UC(0x017A),                     # ź Latin Small Letter Z with Acute
    C("Shift-A"):               UC(0x00C1),                     # Á Latin Capital Letter A with Acute
    C("Shift-C"):               UC(0x0106),                     # Ć Latin Capital Letter C with Acute
    C("Shift-E"):               UC(0x00C9),                     # É Latin Capital Letter E with Acute
    C("Shift-G"):               UC(0x01F4),                     # Ǵ Latin Capital Letter G with Acute
    C("Shift-I"):               UC(0x00CD),                     # Í Latin Capital Letter I with Acute
    C("Shift-M"):               UC(0x1E3E),                     # Ḿ Latin Capital Letter M with Acute
    C("Shift-N"):               UC(0x0143),                     # Ń Latin Capital Letter N with Acute
    C("Shift-O"):               UC(0x00D3),                     # Ó Latin Capital Letter O with Acute
    C("Shift-P"):               UC(0x1E54),                     # Ṕ Latin Capital Letter P with Acute
    C("Shift-R"):               UC(0x0154),                     # Ŕ Latin Capital Letter R with Acute
    C("Shift-S"):               UC(0x015A),                     # Ś Latin Capital Letter S with Acute
    C("Shift-W"):               UC(0x1E82),                     # Ẃ Latin Capital Letter W with Acute
    C("Shift-Y"):               UC(0x00DD),                     # Ý Latin Capital Letter Y with Acute
    C("Shift-Z"):               UC(0x0179),                     # Ź Latin Capital Letter Z with Acute
}, when = lambda _: ac_Chr == 0x00B4 and _optspec_ABC is True)

keymap("DK-ABC - Double Grave", {
    # Shift+Option+Y            {U+030F} [uses {U+02F5} Modifier Letter Middle Double Grave Accent]
    # Valid keys:
    # a e i o r u
    # A E I O R U
    C("A"):                     UC(0x0201),                     # ȁ Latin Small Letter A with Double Grave
    C("E"):                     UC(0x0205),                     # ȅ Latin Small Letter E with Double Grave
    C("I"):                     UC(0x0209),                     # ȉ Latin Small Letter I with Double Grave
    C("O"):                     UC(0x020D),                     # ȍ Latin Small Letter O with Double Grave
    C("R"):                     UC(0x0211),                     # ȑ Latin Small Letter R with Double Grave
    C("U"):                     UC(0x0215),                     # ȕ Latin Small Letter U with Double Grave
    C("Shift-A"):               UC(0x0200),                     # Ȁ Latin Capital Letter A with Double Grave
    C("Shift-E"):               UC(0x0204),                     # Ȅ Latin Capital Letter E with Double Grave
    C("Shift-I"):               UC(0x0208),                     # Ȉ Latin Capital Letter I with Double Grave
    C("Shift-O"):               UC(0x020C),                     # Ȍ Latin Capital Letter O with Double Grave
    C("Shift-R"):               UC(0x0210),                     # Ȑ Latin Capital Letter R with Double Grave
    C("Shift-U"):               UC(0x0214),                     # Ȕ Latin Capital Letter U with Double Grave
}, when = lambda _: (ac_Chr == 0x030F or ac_Chr == 0x02F5) and _optspec_ABC is True)
# }, when = lambda _: ac_Chr == 0x030F and _optspecialchars_ABC is True) # spacing issues with {U+030F}

keymap("DK-ABC - Umlaut/Diaeresis", {
    # Option+U                  {U+00A8}
    # Valid keys:
    # a e h i o t u w x y
    # A E H I O T U W X Y
    C("A"):                     UC(0x00E4),                     # ä Latin Small Letter A with Diaeresis
    C("E"):                     UC(0x00EB),                     # ë Latin Small Letter E with Diaeresis
    C("H"):                     UC(0x1E27),                     # ḧ Latin Small Letter H with Diaeresis
    C("I"):                     UC(0x00EF),                     # ï Latin Small Letter I with Diaeresis
    C("O"):                     UC(0x00F6),                     # ö Latin Small Letter O with Diaeresis
    C("T"):                     UC(0x1E97),                     # ẗ Latin Small Letter T with Diaeresis
    C("U"):                     UC(0x00FC),                     # ü Latin Small Letter U with Diaeresis
    C("W"):                     UC(0x1E85),                     # ẅ Latin Small Letter W with Diaeresis
    C("X"):                     UC(0x1E8D),                     # ẍ Latin Small Letter X with Diaeresis
    C("Y"):                     UC(0x00FF),                     # ÿ Latin Small Letter Y with Diaeresis
    C("Shift-A"):               UC(0x00C4),                     # Ä Latin Capital Letter A with Diaeresis
    C("Shift-E"):               UC(0x00CB),                     # Ë Latin Capital Letter E with Diaeresis
    C("Shift-H"):               UC(0x1E26),                     # Ḧ Latin Capital Letter H with Diaeresis
    C("Shift-I"):               UC(0x00CF),                     # Ï Latin Capital Letter I with Diaeresis
    C("Shift-O"):               UC(0x00D6),                     # Ö Latin Capital Letter O with Diaeresis
    C("Shift-T"):              [UC(0x0054),UC(0x0308)],         # T̈ Latin Capital Letter T with Diaeresis
    C("Shift-U"):               UC(0x00DC),                     # Ü Latin Capital Letter U with Diaeresis
    C("Shift-W"):               UC(0x1E84),                     # Ẅ Latin Capital Letter W with Diaeresis
    C("Shift-X"):               UC(0x1E8C),                     # Ẍ Latin Capital Letter X with Diaeresis
    C("Shift-Y"):               UC(0x0178),                     # Ÿ Latin Capital Letter Y with Diaeresis
}, when = lambda _: ac_Chr == 0x00A8 and _optspec_ABC is True)

keymap("DK-ABC - Apostrophe/Horn", {
    # Option+I                  {U+02BC}
    # Valid keys:
    # o u
    # O U
    C("O"):                     UC(0x01A1),                     # ơ Latin Small Letter O with Horn
    C("U"):                     UC(0x01B0),                     # ư Latin Small Letter U with Horn
    C("Shift-O"):               UC(0x01A0),                     # Ơ Latin Capital Letter O with Horn
    C("Shift-U"):               UC(0x01AF),                     # Ư Latin Capital Letter U with Horn
}, when = lambda _: ac_Chr == 0x02BC and _optspec_ABC is True)

keymap("DK-ABC - Comma Below", {
    # Option+P                  {U+002C}
    # Valid keys:
    # s t
    # S T
    C("S"):                     UC(0x0219),                     # ș Latin Small Letter S with Comma Below
    C("T"):                     UC(0x021B),                     # ț Latin Small Letter T with Comma Below
    C("Shift-S"):               UC(0x0218),                     # Ș Latin Capital Letter S with Comma Below
    C("Shift-T"):               UC(0x021A),                     # Ț Latin Capital Letter T with Comma Below
}, when = lambda _: ac_Chr == 0x002C and _optspec_ABC is True)

keymap("DK-ABC - Macron/Line Above", {
    # Option+A                  {U+00AF}
    # Valid keys:
    # a e g i l o r s v y z
    # A E G I L O R S V Y Z
    C("A"):                     UC(0x0101),                     # ā Latin Small Letter A with Macron
    C("E"):                     UC(0x0113),                     # ē Latin Small Letter E with Macron
    C("G"):                     UC(0x1E21),                     # ḡ Latin Small Letter G with Macron
    C("I"):                     UC(0x012B),                     # ī Latin Small Letter I with Macron
    C("L"):         [UC(0x006C),UC(0x0304),UC(0x0323)],         # ḹ Latin Small Letter L w/Macron and Dot Below
    C("O"):                     UC(0x014D),                     # ō Latin Small Letter O with Macron
    C("R"):         [UC(0x0072),UC(0x0304),UC(0x0323)],         # ṝ Latin Small Letter R w/Macron and Dot Below
    C("S"):                    [UC(0x0073),UC(0x0304)],         # s̄ Latin Small Letter S with Macron
    C("V"):                     UC(0x01D6),                     # ǖ Latin Small Letter U with Diaeresis and Macron
    C("Y"):                     UC(0x0233),                     # ȳ Latin Small Letter Y with Macron
    C("Z"):                    [UC(0x007A),UC(0x0304)],         # z̄ Latin Small Letter Z with Macron
    C("Shift-A"):               UC(0x0100),                     # Ā Latin Capital Letter A with Macron
    C("Shift-E"):               UC(0x0112),                     # Ē Latin Capital Letter E with Macron
    C("Shift-G"):               UC(0x1E20),                     # Ḡ Latin Capital Letter G with Macron
    C("Shift-I"):               UC(0x012A),                     # Ī Latin Capital Letter I with Macron
    C("Shift-L"):   [UC(0x004C),UC(0x0304),UC(0x0323)],         # Ḹ Latin Capital Letter L w/Macron and Dot Below
    C("Shift-O"):               UC(0x014C),                     # Ō Latin Capital Letter O with Macron
    C("Shift-R"):   [UC(0x0052),UC(0x0304),UC(0x0323)],         # Ṝ Latin Capital Letter R w/Macron and Dot Below
    C("Shift-S"):              [UC(0x0053),UC(0x0304)],         # S̄ Latin Capital Letter S with Macron
    C("Shift-V"):               UC(0x01D5),                     # Ǖ Latin Capital Letter U with Diaeresis and Macron
    C("Shift-Y"):               UC(0x0232),                     # Ȳ Latin Capital Letter Y with Macron
    C("Shift-Z"):              [UC(0x005A),UC(0x0304)],         # Z̄ Latin Capital Letter Z with Macron
}, when = lambda _: ac_Chr == 0x00AF and _optspec_ABC is True)

keymap("DK-ABC - Inverted Breve", {
    # Shift+Option+S            {U+0311}    [uses {U+1D16} as a substitute]
    # Valid keys:
    # a e i o r u
    # A E I O R U 
    C("A"):                     UC(0x0203),                     # ȃ Latin Small Letter A with Inverted Breve
    C("E"):                     UC(0x0207),                     # ȇ Latin Small Letter E with Inverted Breve
    C("I"):                     UC(0x020B),                     # ȋ Latin Small Letter I with Inverted Breve
    C("O"):                     UC(0x020F),                     # ȏ Latin Small Letter O with Inverted Breve
    C("R"):                     UC(0x0213),                     # ȓ Latin Small Letter R with Inverted Breve
    C("U"):                     UC(0x0217),                     # ȗ Latin Small Letter U with Inverted Breve
    C("Shift-A"):               UC(0x0202),                     # Ȃ Latin Capital Letter A with Inverted Breve
    C("Shift-E"):               UC(0x0206),                     # Ȇ Latin Capital Letter E with Inverted Breve
    C("Shift-I"):               UC(0x020A),                     # Ȋ Latin Capital Letter I with Inverted Breve
    C("Shift-O"):               UC(0x020E),                     # Ȏ Latin Capital Letter O with Inverted Breve
    C("Shift-R"):               UC(0x0212),                     # Ȓ Latin Capital Letter R with Inverted Breve
    C("Shift-U"):               UC(0x0216),                     # Ȗ Latin Capital Letter U with Inverted Breve
}, when = lambda _: (ac_Chr == 0x0311 or ac_Chr == 0x1D16) and _optspec_ABC is True)

keymap("DK-ABC - Tilde Below", {
    # Shift+Option+F            {U+0330}    [uses {U+02F7} as a substitute]
    # Valid keys:
    # e i u
    # E I U
    C("E"):                     UC(0x1E1B),                     # ḛ Latin Small Letter E with Tilde Below
    C("I"):                     UC(0x1E2D),                     # ḭ Latin Small Letter I with Tilde Below
    C("U"):                     UC(0x1E75),                     # ṵ Latin Small Letter U with Tilde Below
    C("Shift-E"):               UC(0x1E1A),                     # Ḛ Latin Capital Letter E with Tilde Below
    C("Shift-I"):               UC(0x1E2C),                     # Ḭ Latin Capital Letter I with Tilde Below
    C("Shift-U"):               UC(0x1E74),                     # Ṵ Latin Capital Letter U with Tilde Below
}, when = lambda _: (ac_Chr == 0x0330 or ac_Chr == 0x02F7) and _optspec_ABC is True)

keymap("DK-ABC - Caret/Circumflex Below", {
    # Shift+Option+G            {U+2038}
    # Valid keys:
    # d e l n t u
    # D E L N T U
    C("D"):                     UC(0x1E13),                     # ḓ Latin Small Letter D with Circumflex Below
    C("E"):                     UC(0x1E19),                     # ḙ Latin Small Letter E with Circumflex Below
    C("L"):                     UC(0x1E3D),                     # ḽ Latin Small Letter L with Circumflex Below
    C("N"):                     UC(0x1E4B),                     # ṋ Latin Small Letter N with Circumflex Below
    C("T"):                     UC(0x1E71),                     # ṱ Latin Small Letter T with Circumflex Below
    C("U"):                     UC(0x1E77),                     # ṷ Latin Small Letter U with Circumflex Below
    C("Shift-D"):               UC(0x1E12),                     # Ḓ Latin Capital Letter D with Circumflex Below
    C("Shift-E"):               UC(0x1E18),                     # Ḙ Latin Capital Letter E with Circumflex Below
    C("Shift-L"):               UC(0x1E3C),                     # Ḽ Latin Capital Letter L with Circumflex Below
    C("Shift-N"):               UC(0x1E4A),                     # Ṋ Latin Capital Letter N with Circumflex Below
    C("Shift-T"):               UC(0x1E70),                     # Ṱ Latin Capital Letter T with Circumflex Below
    C("Shift-U"):               UC(0x1E76),                     # Ṷ Latin Capital Letter U with Circumflex Below
}, when = lambda _: ac_Chr == 0x2038 and _optspec_ABC is True)

keymap("DK-ABC - Low Macron/Line Below", {
    # Option+H                  {U+02CD}
    # Valid keys:
    # b d h k l n r t z
    # B D H K L N R T Z 
    C("B"):                     UC(0x1E07),                     # ḇ Latin Small Letter B with Line Below 
    C("D"):                     UC(0x1E0F),                     # ḏ Latin Small Letter D with Line Below 
    C("H"):                     UC(0x1E96),                     # ẖ Latin Small Letter H with Line Below 
    C("K"):                     UC(0x1E35),                     # ḵ Latin Small Letter K with Line Below 
    C("L"):                     UC(0x1E3B),                     # ḻ Latin Small Letter L with Line Below 
    C("N"):                     UC(0x1E49),                     # ṉ Latin Small Letter N with Line Below 
    C("R"):                     UC(0x1E5F),                     # ṟ Latin Small Letter R with Line Below 
    C("T"):                     UC(0x1E6F),                     # ṯ Latin Small Letter T with Line Below 
    C("Z"):                     UC(0x1E95),                     # ẕ Latin Small Letter Z with Line Below 
    C("Shift-B"):               UC(0x1E06),                     # Ḇ Latin Capital Letter B with Line Below 
    C("Shift-D"):               UC(0x1E0E),                     # Ḏ Latin Capital Letter D with Line Below 
    C("Shift-H"):              [UC(0x0048),UC(0x0331)],         # H̱ Latin Capital Letter H with Line Below
    C("Shift-K"):               UC(0x1E34),                     # Ḵ Latin Capital Letter K with Line Below 
    C("Shift-L"):               UC(0x1E3A),                     # Ḻ Latin Capital Letter L with Line Below 
    C("Shift-N"):               UC(0x1E48),                     # Ṉ Latin Capital Letter N with Line Below 
    C("Shift-R"):               UC(0x1E5E),                     # Ṟ Latin Capital Letter R with Line Below 
    C("Shift-T"):               UC(0x1E6E),                     # Ṯ Latin Capital Letter T with Line Below 
    C("Shift-Z"):               UC(0x1E94),                     # Ẕ Latin Capital Letter Z with Line Below 
}, when = lambda _: ac_Chr == 0x02CD and _optspec_ABC is True)

keymap("DK-ABC - Double Acute", {
    # Option+J                  {U+02DD}
    # Valid keys:
    # o u
    # O U
    C("O"):                     UC(0x0151),                     # ő Latin Small Letter O with Double Acute
    C("U"):                     UC(0x0171),                     # ű Latin Small Letter U with Double Acute
    C("Shift-O"):               UC(0x0150),                     # Ő Latin Capital Letter O with Double Acute
    C("Shift-U"):               UC(0x0170),                     # Ű Latin Capital Letter U with Double Acute
}, when = lambda _: ac_Chr == 0x02DD and _optspec_ABC is True)

keymap("DK-ABC - Ring Above", {
    # Option+K                  {U+02DA}
    # Valid keys:
    # a e o u w y
    # A E O U W Y 
    C("A"):                     UC(0x00E5),                     # å Latin Small Letter A with Ring Above
    C("E"):                    [UC(0x0065),UC(0x030A)],         # e̊ Latin Small Letter E with Ring Above
    C("O"):                    [UC(0x006F),UC(0x030A)],         # o̊ Latin Small Letter O with Ring Above
    C("U"):                     UC(0x016F),                     # ů Latin Small Letter U with Ring Above
    C("W"):                     UC(0x1E98),                     # ẘ Latin Small Letter W with Ring Above
    C("Y"):                     UC(0x1E99),                     # ẙ Latin Small Letter Y with Ring Above
    C("Shift-A"):               UC(0x00C5),                     # Å Latin Capital Letter A with Ring Above
    C("Shift-E"):              [UC(0x0045),UC(0x030A)],         # E̊ Latin Capital Letter E with Ring Above
    C("Shift-O"):              [UC(0x004F),UC(0x030A)],         # O̊ Latin Capital Letter O with Ring Above
    C("Shift-U"):               UC(0x016E),                     # Ů Latin Capital Letter U with Ring Above
    C("Shift-W"):              [UC(0x0057),UC(0x030A)],         # W̊ Latin Capital Letter W with Ring Above
    C("Shift-Y"):              [UC(0x0059),UC(0x030A)],         # Y̊ Latin Capital Letter Y with Ring Above
}, when = lambda _: ac_Chr == 0x02DA and _optspec_ABC is True)

keymap("DK-ABC - Stroke/Hyphen-Minus", {
    # Option+L                  {U+002D}
    # Valid keys:
    # b d g h i l o t u z
    #   D G H I L O T   Z 
    C("B"):                     UC(0x0180),                     # ƀ Latin Small Letter B with Stroke
    C("D"):                     UC(0x0111),                     # đ Latin Small Letter D with Stroke
    C("G"):                     UC(0x01E5),                     # ǥ Latin Small Letter G with Stroke
    C("H"):                     UC(0x0127),                     # ħ Latin Small Letter H with Stroke
    C("I"):                     UC(0x0268),                     # ɨ Latin Small Letter I with Stroke
    C("L"):                     UC(0x0142),                     # ł Latin Small Letter L with Stroke
    C("O"):                     UC(0x0275),                     # ɵ Latin Small Letter Barred O
    C("T"):                     UC(0x0167),                     # ŧ Latin Small Letter T with Stroke
    C("U"):                     UC(0x0289),                     # ʉ Latin Small Letter U Bar
    C("Z"):                     UC(0x01B6),                     # ƶ Latin Small Letter Z with Stroke
    C("Shift-D"):               UC(0x0110),                     # Đ Latin Capital Letter D with Stroke
    C("Shift-G"):               UC(0x01E4),                     # Ǥ Latin Capital Letter G with Stroke
    C("Shift-H"):               UC(0x0126),                     # Ħ Latin Capital Letter H with Stroke
    C("Shift-I"):               UC(0x0197),                     # Ɨ Latin Capital Letter I with Stroke
    C("Shift-L"):               UC(0x0141),                     # Ł Latin Capital Letter L with Stroke
    C("Shift-O"):               UC(0x019F),                     # Ɵ Latin Capital Letter O with Middle Tilde
    C("Shift-T"):               UC(0x0166),                     # Ŧ Latin Capital Letter T with Stroke
    C("Shift-Z"):               UC(0x01B5),                     # Ƶ Latin Capital Letter Z with Stroke
}, when = lambda _: ac_Chr == 0x002D and _optspec_ABC is True)

keymap("DK-ABC - Numero Sign", {
    # Shift+Option+Semicolon    {U+2116}
    # Valid keys:
    # 2 3 5 6 7 8 (digits with Option)
    # 2 3 5 6   8 (digits with Shift+Option)
    # a c e g h j k m n q r s u v w y z (letters with Option)
    # A C E G H J K M N Q R   U   W Y Z (letters with Shift+Option)
    C("3"):                     UC(0x025B),                     # ɛ  Latin Small Letter Open E
    C("5"):                     UC(0x01BD),                     # ƽ  Latin Small Letter Tone Five
    C("2"):                     UC(0x01A8),                     # ƨ  Latin Small Letter Tone Two
    C("6"):                     UC(0x0185),                     # ƅ  Latin Small Letter Tone Six
    C("7"):                     UC(0x204A),                     # ⁊  Tironian Sign Et 
    C("8"):                     UC(0x0223),                     # ȣ  Latin Small Letter Ou
    C("Shift-2"):               UC(0x01A7),                     # Ƨ  Latin Capital Letter Tone Two
    C("Shift-3"):               UC(0x0190),                     # Ɛ  Latin Capital Letter Open E
    C("Shift-5"):               UC(0x01BC),                     # Ƽ  Latin Capital Letter Tone Five
    C("Shift-6"):               UC(0x0184),                     # Ƅ  Latin Capital Letter Tone Six
    C("Shift-8"):               UC(0x0222),                     # Ȣ  Latin Capital Letter Ou
    C("a"):                     UC(0x0259),                     # ə  Latin Small Letter Schwa
    C("c"):                     UC(0x0254),                     # ɔ  Latin Small Letter Open O
    C("e"):                     UC(0x01DD),                     # ǝ  Latin Small Letter Turned E
    C("g"):                     UC(0x0263),                     # ɣ  Latin Small Letter Gamma
    C("h"):                     UC(0x0195),                     # ƕ  Latin Small Letter Hv
    C("j"):                     UC(0x019E),                     # ƞ  Latin Small Letter N with Long Right Leg
    C("k"):                     UC(0x0138),                     # ĸ  Latin Small Letter Kra
    C("m"):                     UC(0x026F),                     # ɯ  Latin Small Letter Turned M
    C("n"):                     UC(0x014B),                     # ŋ  Latin Small Letter Eng
    C("q"):                     UC(0x01A3),                     # ƣ  Latin Small Letter Oi
    C("r"):                     UC(0x0280),                     # ʀ  Latin Letter Small Capital R
    C("s"):                     UC(0x017F),                     # ſ  Latin Small Letter Long S
    C("u"):                     UC(0x028A),                     # ʊ  Latin Small Letter Upsilon
    C("v"):                     UC(0x028C),                     # ʌ  Latin Small Letter Turned V
    C("w"):                     UC(0x01BF),                     # ƿ  Latin Letter Wynn
    C("y"):                     UC(0x021D),                     # ȝ  Latin Small Letter Yogh
    C("z"):                     UC(0x0292),                     # ʒ  Latin Small Letter Ezh
    C("Shift-A"):               UC(0x018F),                     # Ə  Latin Capital Letter Schwa
    C("Shift-C"):               UC(0x0186),                     # Ɔ  Latin Capital Letter Open O
    C("Shift-E"):               UC(0x018E),                     # Ǝ  Latin Capital Letter Reversed E
    C("Shift-G"):               UC(0x0194),                     # Ɣ  Latin Capital Letter Gamma
    C("Shift-H"):               UC(0x01F6),                     # Ƕ  Latin Capital Letter Hwair
    C("Shift-J"):               UC(0x0220),                     # Ƞ  Latin Capital Letter N with Long Right Leg
    C("Shift-K"):              [UC(0x004B),UC(0x2019)],         # K’ Latin Capital Letter K with Apostrophe
    C("Shift-M"):               UC(0x019C),                     # Ɯ  Latin Capital Letter Turned M
    C("Shift-N"):               UC(0x014A),                     # Ŋ  Latin Capital Letter Eng
    C("Shift-Q"):               UC(0x01A2),                     # Ƣ  Latin Capital Letter Oi
    C("Shift-R"):               UC(0x01A6),                     # Ʀ  Latin Letter Yr
    C("Shift-U"):               UC(0x01B1),                     # Ʊ  Latin Capital Letter Upsilon
    C("Shift-W"):               UC(0x01F7),                     # Ƿ  Latin Capital Letter Wynn
    C("Shift-Y"):               UC(0x021C),                     # Ȝ  Latin Capital Letter Yogh
    C("Shift-Z"):               UC(0x01B7),                     # Ʒ  Latin Capital Letter Ezh
}, when = lambda _: ac_Chr == 0x2116 and _optspec_ABC is True)

keymap("DK-ABC - Hook Above/Glottal Stop", {
    # Option+Z                  {U+02C0}
    # Valid keys:
    # a e i o u y
    # A E I O U Y 
    C("A"):                     UC(0x1EA3),                     # ả  Latin Small Letter A with Hook Above
    C("E"):                     UC(0x1EBB),                     # ẻ  Latin Small Letter E with Hook Above
    C("I"):                     UC(0x1EC9),                     # ỉ  Latin Small Letter I with Hook Above
    C("O"):                     UC(0x1ECF),                     # ỏ  Latin Small Letter O with Hook Above
    C("U"):                     UC(0x1EE7),                     # ủ  Latin Small Letter U with Hook Above
    C("Y"):                     UC(0x1EF7),                     # ỷ  Latin Small Letter Y with Hook Above
    C("Shift-A"):               UC(0x1EA2),                     # Ả  Latin Small Letter A with Hook Above
    C("Shift-E"):               UC(0x1EBA),                     # Ẻ  Latin Small Letter E with Hook Above
    C("Shift-I"):               UC(0x1EC8),                     # Ỉ  Latin Small Letter I with Hook Above
    C("Shift-O"):               UC(0x1ECE),                     # Ỏ  Latin Small Letter O with Hook Above
    C("Shift-U"):               UC(0x1EE6),                     # Ủ  Latin Small Letter U with Hook Above
    C("Shift-Y"):               UC(0x1EF6),                     # Ỷ  Latin Small Letter Y with Hook Above
}, when = lambda _: ac_Chr == 0x02C0 and _optspec_ABC is True)

keymap("DK-ABC - Dot Below", {
    # Option+X                  {U+002E}
    # Valid keys:
    # a b d e h i k l m n o r s t u v w y z
    # A B D E H I K L M N O R S T U V W Y Z 
    C("A"):                     UC(0x1EA1),                     # ạ Latin Small Letter A with Dot Below
    C("B"):                     UC(0x1E05),                     # ḅ Latin Small Letter B with Dot Below
    C("D"):                     UC(0x1E0D),                     # ḍ Latin Small Letter D with Dot Below
    C("E"):                     UC(0x1EB9),                     # ẹ Latin Small Letter E with Dot Below
    C("H"):                     UC(0x1E25),                     # ḥ Latin Small Letter H with Dot Below
    C("I"):                     UC(0x1ECB),                     # ị Latin Small Letter I with Dot Below
    C("K"):                     UC(0x1E33),                     # ḳ Latin Small Letter K with Dot Below
    C("L"):                     UC(0x1E37),                     # ḷ Latin Small Letter L with Dot Below
    C("M"):                     UC(0x1E43),                     # ṃ Latin Small Letter M with Dot Below
    C("N"):                     UC(0x1E47),                     # ṇ Latin Small Letter N with Dot Below
    C("O"):                     UC(0x1ECD),                     # ọ Latin Small Letter O with Dot Below
    C("R"):                     UC(0x1E5B),                     # ṛ Latin Small Letter R with Dot Below
    C("S"):                     UC(0x1E63),                     # ṣ Latin Small Letter S with Dot Below
    C("T"):                     UC(0x1E6D),                     # ṭ Latin Small Letter T with Dot Below
    C("U"):                     UC(0x1EE5),                     # ụ Latin Small Letter U with Dot Below
    C("V"):                     UC(0x1E7F),                     # ṿ Latin Small Letter V with Dot Below
    C("W"):                     UC(0x1E89),                     # ẉ Latin Small Letter W with Dot Below
    C("Y"):                     UC(0x1EF5),                     # ỵ Latin Small Letter Y with Dot Below
    C("Z"):                     UC(0x1E93),                     # ẓ Latin Small Letter Z with Dot Below
    C("Shift-A"):               UC(0x1EA0),                     # Ạ Latin Capital Letter A with Dot Below
    C("Shift-B"):               UC(0x1E04),                     # Ḅ Latin Capital Letter B with Dot Below
    C("Shift-D"):               UC(0x1E0C),                     # Ḍ Latin Capital Letter D with Dot Below
    C("Shift-E"):               UC(0x1EB8),                     # Ẹ Latin Capital Letter E with Dot Below
    C("Shift-H"):               UC(0x1E24),                     # Ḥ Latin Capital Letter H with Dot Below
    C("Shift-I"):               UC(0x1ECA),                     # Ị Latin Capital Letter I with Dot Below
    C("Shift-K"):               UC(0x1E32),                     # Ḳ Latin Capital Letter K with Dot Below
    C("Shift-L"):               UC(0x1E36),                     # Ḷ Latin Capital Letter L with Dot Below
    C("Shift-M"):               UC(0x1E42),                     # Ṃ Latin Capital Letter M with Dot Below
    C("Shift-N"):               UC(0x1E46),                     # Ṇ Latin Capital Letter N with Dot Below
    C("Shift-O"):               UC(0x1ECC),                     # Ọ Latin Capital Letter O with Dot Below
    C("Shift-R"):               UC(0x1E5A),                     # Ṛ Latin Capital Letter R with Dot Below
    C("Shift-S"):               UC(0x1E62),                     # Ṣ Latin Capital Letter S with Dot Below
    C("Shift-T"):               UC(0x1E6C),                     # Ṭ Latin Capital Letter T with Dot Below
    C("Shift-U"):               UC(0x1EE4),                     # Ụ Latin Capital Letter U with Dot Below
    C("Shift-V"):               UC(0x1E7E),                     # Ṿ Latin Capital Letter V with Dot Below
    C("Shift-W"):               UC(0x1E88),                     # Ẉ Latin Capital Letter W with Dot Below
    C("Shift-Y"):               UC(0x1EF4),                     # Ỵ Latin Capital Letter Y with Dot Below
    C("Shift-Z"):               UC(0x1E92),                     # Ẓ Latin Capital Letter Z with Dot Below
}, when = lambda _: ac_Chr == 0x002E and _optspec_ABC is True)

keymap("DK-ABC - Cedilla/Cedille", {
    # Option+C                  {U+00B8}
    # Valid keys:
    # c d e g h k l n r s t z
    # C D E G H K L N R S T Z 
    C("C"):                     UC(0x00E7),                     # ç Latin Small Letter C with Cedilla
    C("D"):                     UC(0x1E11),                     # ḑ Latin Small Letter D with Cedilla
    C("E"):                     UC(0x0229),                     # ȩ Latin Small Letter E with Cedilla
    C("G"):                     UC(0x0123),                     # ģ Latin Small Letter G with Cedilla
    C("H"):                     UC(0x1E29),                     # ḩ Latin Small Letter H with Cedilla
    C("K"):                     UC(0x0137),                     # ķ Latin Small Letter K with Cedilla
    C("L"):                     UC(0x013C),                     # ļ Latin Small Letter L with Cedilla
    C("N"):                     UC(0x0146),                     # ņ Latin Small Letter N with Cedilla
    C("R"):                     UC(0x0157),                     # ŗ Latin Small Letter R with Cedilla
    C("S"):                     UC(0x015F),                     # ş Latin Small Letter S with Cedilla
    C("T"):                     UC(0x0163),                     # ţ Latin Small Letter T with Cedilla
    C("Z"):                    [UC(0x007A),UC(0x0327)],         # z̧ Latin Small Letter Z with Cedilla
    C("Shift-C"):               UC(0x00C7),                     # Ç Latin Capital Letter C with Cedilla
    C("Shift-D"):               UC(0x1E10),                     # Ḑ Latin Capital Letter D with Cedilla
    C("Shift-E"):               UC(0x0228),                     # Ȩ Latin Capital Letter E with Cedilla
    C("Shift-G"):               UC(0x0122),                     # Ģ Latin Capital Letter G with Cedilla
    C("Shift-H"):               UC(0x1E28),                     # Ḩ Latin Capital Letter H with Cedilla
    C("Shift-K"):               UC(0x0136),                     # Ķ Latin Capital Letter K with Cedilla
    C("Shift-L"):               UC(0x013B),                     # Ļ Latin Capital Letter L with Cedilla
    C("Shift-N"):               UC(0x0145),                     # Ņ Latin Capital Letter N with Cedilla
    C("Shift-R"):               UC(0x0156),                     # Ŗ Latin Capital Letter R with Cedilla
    C("Shift-S"):               UC(0x015E),                     # Ş Latin Capital Letter S with Cedilla
    C("Shift-T"):               UC(0x0162),                     # Ţ Latin Capital Letter T with Cedilla
    C("Shift-Z"):              [UC(0x005A),UC(0x0327)],         # Z̧ Latin Capital Letter Z with Cedilla
}, when = lambda _: ac_Chr == 0x00B8 and _optspec_ABC is True)

keymap("DK-ABC - Caron/hacek", {
    # Option+V                  {U+02C7}
    # Valid keys:
    # a c d e g h i j k l n o r s t u v x z
    # A C D E G H I J K L N O R S T U V X Z 
    C("A"):                     UC(0x01CE),                     # ǎ Latin Small Letter A with Caron
    C("C"):                     UC(0x010D),                     # č Latin Small Letter C with Caron
    C("D"):                     UC(0x010F),                     # ď Latin Small Letter D with Caron
    C("E"):                     UC(0x011B),                     # ě Latin Small Letter E with Caron
    C("G"):                     UC(0x01E7),                     # ǧ Latin Small Letter G with Caron
    C("H"):                     UC(0x021F),                     # ȟ Latin Small Letter H with Caron
    C("I"):                     UC(0x01D0),                     # ǐ Latin Small Letter I with Caron
    C("J"):                     UC(0x01F0),                     # ǰ Latin Small Letter J with Caron
    C("K"):                     UC(0x01E9),                     # ǩ Latin Small Letter K with Caron
    C("L"):                     UC(0x013E),                     # ľ Latin Small Letter L with Caron
    C("N"):                     UC(0x0148),                     # ň Latin Small Letter N with Caron
    C("O"):                     UC(0x01D2),                     # ǒ Latin Small Letter O with Caron
    C("R"):                     UC(0x0159),                     # ř Latin Small Letter R with Caron
    C("S"):                     UC(0x0161),                     # š Latin Small Letter S with Caron
    C("T"):                     UC(0x0165),                     # ť Latin Small Letter T with Caron
    C("U"):                     UC(0x01D4),                     # ǔ Latin Small Letter U with Caron
    C("V"):                     UC(0x01DA),                     # ǚ Latin Small Letter U w/Diaeresis and Caron
    C("X"):                    [UC(0x0292),UC(0x030C)],         # ǯ Latin Small Letter Ezh with Caron
    C("Z"):                     UC(0x017E),                     # ž Latin Small Letter Z with Caron
    C("Shift-A"):               UC(0x01CD),                     # Ǎ Latin Capital Letter A with Caron
    C("Shift-C"):               UC(0x010C),                     # Č Latin Capital Letter C with Caron
    C("Shift-D"):               UC(0x010E),                     # Ď Latin Capital Letter D with Caron
    C("Shift-E"):               UC(0x011A),                     # Ě Latin Capital Letter E with Caron
    C("Shift-G"):               UC(0x01E6),                     # Ǧ Latin Capital Letter G with Caron
    C("Shift-H"):               UC(0x021E),                     # Ȟ Latin Capital Letter H with Caron
    C("Shift-I"):               UC(0x01CF),                     # Ǐ Latin Capital Letter I with Caron
    C("Shift-J"):              [UC(0x004A),UC(0x030C)],         # J̌ Latin Capital Letter J with Caron
    C("Shift-K"):               UC(0x01E8),                     # Ǩ Latin Capital Letter K with Caron
    C("Shift-L"):               UC(0x013D),                     # Ľ Latin Capital Letter L with Caron
    C("Shift-N"):               UC(0x0147),                     # Ň Latin Capital Letter N with Caron
    C("Shift-O"):               UC(0x01D1),                     # Ǒ Latin Capital Letter O with Caron
    C("Shift-R"):               UC(0x0158),                     # Ř Latin Capital Letter R with Caron
    C("Shift-S"):               UC(0x0160),                     # Š Latin Capital Letter S with Caron
    C("Shift-T"):               UC(0x0164),                     # Ť Latin Capital Letter T with Caron
    C("Shift-U"):               UC(0x01D3),                     # Ǔ Latin Capital Letter U with Caron
    C("Shift-V"):               UC(0x01D9),                     # Ǚ Latin Capital Letter U w/Diaeresis and Caron
    C("Shift-X"):              [UC(0x01B7),UC(0x030C)],         # Ǯ Latin Capital Letter Ezh with Caron
    C("Shift-Z"):               UC(0x017D),                     # Ž Latin Capital Letter Z with Caron
}, when = lambda _: ac_Chr == 0x02C7 and _optspec_ABC is True)

keymap("DK-ABC - Breve", {
    # Option+B                  {U+02D8}
    # Valid keys:
    # a e g h i o u
    # A E G H I O U 
    C("A"):                     UC(0x0103),                     # ă Latin Small Letter A with Breve
    C("E"):                     UC(0x0115),                     # ĕ Latin Small Letter E with Breve
    C("G"):                     UC(0x011F),                     # ğ Latin Small Letter G with Breve
    C("H"):                     UC(0x1E2B),                     # ḫ Latin Small Letter H with Breve Below
    C("I"):                     UC(0x012D),                     # ĭ Latin Small Letter I with Breve
    C("O"):                     UC(0x014F),                     # ŏ Latin Small Letter O with Breve
    C("U"):                     UC(0x016D),                     # ŭ Latin Small Letter U with Breve
    C("Shift-A"):               UC(0x0102),                     # Ă Latin Capital Letter A with Breve
    C("Shift-E"):               UC(0x0114),                     # Ĕ Latin Capital Letter E with Breve
    C("Shift-G"):               UC(0x011E),                     # Ğ Latin Capital Letter G with Breve
    C("Shift-H"):               UC(0x1E2A),                     # Ḫ Latin Capital Letter H with Breve Below
    C("Shift-I"):               UC(0x012C),                     # Ĭ Latin Capital Letter I with Breve
    C("Shift-O"):               UC(0x014E),                     # Ŏ Latin Capital Letter O with Breve
    C("Shift-U"):               UC(0x016C),                     # Ŭ Latin Capital Letter U with Breve
}, when = lambda _: ac_Chr == 0x02D8 and _optspec_ABC is True)

keymap("DK-ABC - Tilde", {
    # Option+N                  {U+02DC}
    # Valid keys:
    # a e i n o u v y
    # A E I N O U V Y 
    C("A"):                     UC(0x00E3),                     # ã Latin Small Letter A with Tilde
    C("E"):                     UC(0x1EBD),                     # ẽ Latin Small Letter E with Tilde
    C("I"):                     UC(0x0129),                     # ĩ Latin Small Letter I with Tilde
    C("N"):                     UC(0x00F1),                     # ñ Latin Small Letter N with Tilde
    C("O"):                     UC(0x00F5),                     # õ Latin Small Letter O with Tilde
    C("U"):                     UC(0x0169),                     # ũ Latin Small Letter U with Tilde
    C("V"):                     UC(0x1E7D),                     # ṽ Latin Small Letter V with Tilde
    C("Y"):                     UC(0x1EF9),                     # ỹ Latin Small Letter Y with Tilde
    C("Shift-A"):               UC(0x00C3),                     # Ã Latin Capital Letter A with Tilde
    C("Shift-E"):               UC(0x1EBC),                     # Ẽ Latin Capital Letter E with Tilde
    C("Shift-I"):               UC(0x0128),                     # Ĩ Latin Capital Letter I with Tilde
    C("Shift-N"):               UC(0x00D1),                     # Ñ Latin Capital Letter N with Tilde
    C("Shift-O"):               UC(0x00D5),                     # Õ Latin Capital Letter O with Tilde
    C("Shift-U"):               UC(0x0168),                     # Ũ Latin Capital Letter U with Tilde
    C("Shift-V"):               UC(0x1E7C),                     # Ṽ Latin Capital Letter V with Tilde
    C("Shift-Y"):               UC(0x1EF8),                     # Ỹ Latin Capital Letter Y with Tilde
}, when = lambda _: ac_Chr == 0x02DC and _optspec_ABC is True)

keymap("DK-ABC - Ogonek", {
    # Option+M                  {U+02DB}
    # Valid keys:
    # a e i o u
    # A E I O U 
    C("A"):                     UC(0x0105),                     # ą Latin Small Letter A with Ogonek
    C("E"):                     UC(0x0119),                     # ę Latin Small Letter E with Ogonek
    C("I"):                     UC(0x012F),                     # į Latin Small Letter I with Ogonek
    C("O"):                     UC(0x01EB),                     # ǫ Latin Small Letter O with Ogonek
    C("U"):                     UC(0x0173),                     # ų Latin Small Letter U with Ogonek
    C("Shift-A"):               UC(0x0104),                     # Ą Latin Capital Letter A with Ogonek
    C("Shift-E"):               UC(0x0118),                     # Ę Latin Capital Letter E with Ogonek
    C("Shift-I"):               UC(0x012E),                     # Į Latin Capital Letter I with Ogonek
    C("Shift-O"):               UC(0x01EA),                     # Ǫ Latin Capital Letter O with Ogonek
    C("Shift-U"):               UC(0x0172),                     # Ų Latin Capital Letter U with Ogonek
}, when = lambda _: ac_Chr == 0x02DB and _optspec_ABC is True)

keymap("DK-ABC - Hook", {
    # Shift+Option+Dot          {U+0294}
    # Valid keys:
    # b c d f g h i k n p q r s t u x y z 
    # B C D F G   I K N P   R S T U X Y Z 
    C("B"):                     UC(0x0253),                     # ɓ Latin Small Letter B with Hook
    C("C"):                     UC(0x0188),                     # ƈ Latin Small Letter C with Hook
    C("D"):                     UC(0x0257),                     # ɗ Latin Small Letter D with Hook
    C("F"):                     UC(0x0192),                     # ƒ Latin Small Letter F with Hook (function symbol)
    C("G"):                     UC(0x0260),                     # ɠ Latin Small Letter G with Hook
    C("H"):                     UC(0x0266),                     # ɦ Latin Small Letter H with Hook
    C("I"):                     UC(0x0269),                     # ɩ Latin Small Letter Iota
    C("K"):                     UC(0x0199),                     # ƙ Latin Small Letter K with Hook
    C("N"):                     UC(0x0272),                     # ɲ Latin Small Letter N with Left Hook
    C("P"):                     UC(0x01A5),                     # ƥ Latin Small Letter P with Hook
    C("Q"):                     UC(0x02A0),                     # ʠ Latin Small Letter Q with Hook
    C("R"):                     UC(0x0288),                     # ʈ Latin Small Letter T with Retroflex Hook
    C("S"):                     UC(0x0283),                     # ʃ Latin Small Letter Esh
    C("T"):                     UC(0x01AD),                     # ƭ Latin Small Letter T with Hook
    C("U"):                     UC(0x028B),                     # ʋ Latin Small Letter V with Hook
    C("X"):                     UC(0x0256),                     # ɖ Latin Small Letter D with Tail
    C("Y"):                     UC(0x01B4),                     # ƴ Latin Small Letter Y with Hook
    C("Z"):                     UC(0x0225),                     # ȥ Latin Small Letter Z with Hook
    C("Shift-B"):               UC(0x0181),                     # Ɓ Latin Capital Letter B with Hook
    C("Shift-C"):               UC(0x0187),                     # Ƈ Latin Capital Letter C with Hook
    C("Shift-D"):               UC(0x018A),                     # Ɗ Latin Capital Letter D with Hook
    C("Shift-F"):               UC(0x0191),                     # Ƒ Latin Capital Letter F with Hook
    C("Shift-G"):               UC(0x0193),                     # Ɠ Latin Capital Letter G with Hook
    C("Shift-I"):               UC(0x0196),                     # Ɩ Latin Capital Letter Iota
    C("Shift-K"):               UC(0x0198),                     # Ƙ Latin Capital Letter K with Hook
    C("Shift-N"):               UC(0x019D),                     # Ɲ Latin Capital Letter N with Left Hook
    C("Shift-P"):               UC(0x01A4),                     # Ƥ Latin Capital Letter P with Hook
    C("Shift-R"):               UC(0x01AE),                     # Ʈ Latin Capital Letter T with Retroflex Hook
    C("Shift-S"):               UC(0x01A9),                     # Ʃ Latin Capital Letter Esh
    C("Shift-T"):               UC(0x01AC),                     # Ƭ Latin Capital Letter T with Hook
    C("Shift-U"):               UC(0x01B2),                     # Ʋ Latin Capital Letter V with Hook
    C("Shift-X"):               UC(0x0189),                     # Ɖ Latin Capital Letter African D
    C("Shift-Y"):               UC(0x01B3),                     # Ƴ Latin Capital Letter Y with Hook
    C("Shift-Z"):               UC(0x0224),                     # Ȥ Latin Capital Letter Z with Hook
}, when = lambda _: ac_Chr == 0x0294 and _optspec_ABC is True)


#######################################
###  DEAD KEYS KEYMAPS - US LAYOUT  ###
#######################################
keymap("DK-US - Grave", {
    # Valid keys:
    # a e i o u
    # A E I O U
    C("A"):                     UC(0x00E0),                     # à Latin Small a with Grave
    C("E"):                     UC(0x00E8),                     # è Latin Small e with Grave
    C("I"):                     UC(0x00EC),                     # ì Latin Small i with Grave
    C("O"):                     UC(0x00F2),                     # ò Latin Small o with Grave
    C("U"):                     UC(0x00F9),                     # ù Latin Small u with Grave
    C("Shift-A"):               UC(0x00C0),                     # À Latin Capital A with Grave
    C("Shift-E"):               UC(0x00C8),                     # È Latin Capital E with Grave
    C("Shift-I"):               UC(0x00CC),                     # Ì Latin Capital I with Grave
    C("Shift-O"):               UC(0x00D2),                     # Ò Latin Capital O with Grave
    C("Shift-U"):               UC(0x00D9),                     # Ù Latin Capital U with Grave
}, when = lambda _: ac_Chr == 0x0060 and _optspec_US is True)

keymap("DK-US - Acute", {
    # Valid keys:
    # a e i o u
    # A E I O U
    C("A"):                     UC(0x00E1),                     # á Latin Small a with Acute
    C("E"):                     UC(0x00E9),                     # é Latin Small e with Acute
    C("I"):                     UC(0x00ED),                     # í Latin Small i with Acute
    C("O"):                     UC(0x00F3),                     # ó Latin Small o with Acute
    C("U"):                     UC(0x00FA),                     # ú Latin Small u with Acute
    C("Shift-A"):               UC(0x00C1),                     # Á Latin Capital A with Acute
    C("Shift-E"):               UC(0x00C9),                     # É Latin Capital E with Acute
    C("Shift-I"):               UC(0x00CD),                     # Í Latin Capital I with Acute
    C("Shift-O"):               UC(0x00D3),                     # Ó Latin Capital O with Acute
    C("Shift-U"):               UC(0x00DA),                     # Ú Latin Capital U with Acute
}, when = lambda _: ac_Chr == 0x00B4 and _optspec_US is True)

keymap("DK-US - Umlaut", {
    # Valid keys:
    # a e i o u y
    # A E I O U Y
    C("A"):                     UC(0x00E4),                     # ä Latin Small a with Umlaut
    C("E"):                     UC(0x00EB),                     # ë Latin Small e with Umlaut
    C("I"):                     UC(0x00EF),                     # ï Latin Small i with Umlaut
    C("O"):                     UC(0x00F6),                     # ö Latin Small o with Umlaut
    C("U"):                     UC(0x00FC),                     # ü Latin Small u with Umlaut
    C("Y"):                     UC(0x00FF),                     # ÿ Latin Small y with Umlaut
    C("Shift-A"):               UC(0x00C4),                     # Ä Latin Capital A with Umlaut
    C("Shift-E"):               UC(0x00CB),                     # Ë Latin Capital E with Umlaut
    C("Shift-I"):               UC(0x00CF),                     # Ï Latin Capital I with Umlaut
    C("Shift-O"):               UC(0x00D6),                     # Ö Latin Capital O with Umlaut
    C("Shift-U"):               UC(0x00DC),                     # Ü Latin Capital U with Umlaut
    C("Shift-Y"):               UC(0x0178),                     # Ÿ Latin Capital Y with Umlaut
}, when = lambda _: ac_Chr == 0x00A8 and _optspec_US is True)

keymap("DK-US - Circumflex", {
    # Valid keys:
    # a e i o u
    # A E I O U
    C("A"):                     UC(0x00E2),                     # â Latin Small a with Circumflex
    C("E"):                     UC(0x00EA),                     # ê Latin Small e with Circumflex
    C("I"):                     UC(0x00EE),                     # î Latin Small i with Circumflex
    C("O"):                     UC(0x00F4),                     # ô Latin Small o with Circumflex
    C("U"):                     UC(0x00FB),                     # û Latin Small u with Circumflex
    C("Shift-A"):               UC(0x00C2),                     # Â Latin Capital A with Circumflex
    C("Shift-E"):               UC(0x00CA),                     # Ê Latin Capital E with Circumflex
    C("Shift-I"):               UC(0x00CE),                     # Î Latin Capital I with Circumflex
    C("Shift-O"):               UC(0x00D4),                     # Ô Latin Capital O with Circumflex
    C("Shift-U"):               UC(0x00DB),                     # Û Latin Capital U with Circumflex
}, when = lambda _: ac_Chr == 0x02C6 and _optspec_US is True)

keymap("DK-US - Tilde", {
    # Valid keys:
    # a n o
    # A N O
    C("A"):                     UC(0x00E3),                     # ã Latin Small a with Tilde
    C("N"):                     UC(0x00F1),                     # ñ Latin Small n with Tilde
    C("O"):                     UC(0x00F5),                     # õ Latin Small o with Tilde
    C("Shift-A"):               UC(0x00C3),                     # Ã Latin Capital A with Tilde
    C("Shift-N"):               UC(0x00D1),                     # Ñ Latin Capital N with Tilde
    C("Shift-O"):               UC(0x00D5),                     # Õ Latin Capital O with Tilde
}, when = lambda _: ac_Chr == 0x02DC and _optspec_US is True)



#################################################################
###                                                           ###
###                                                           ###
###      ███████ ███████  ██████  █████  ██████  ███████      ###
###      ██      ██      ██      ██   ██ ██   ██ ██           ###
###      █████   ███████ ██      ███████ ██████  █████        ###
###      ██           ██ ██      ██   ██ ██      ██           ###
###      ███████ ███████  ██████ ██   ██ ██      ███████      ###
###                                                           ###
###                                                           ###
#################################################################
keymap("Escape actions for dead keys - Overrides for ABC Extended", {

    ###  activate other dead keys correctly while one is active

    # US layout dead keys (not here, see keymap below)

    # ABC Extended layout dead keys
    C("Alt-Grave"):     [getDK(),UC(0x0060),C("Shift-Left"),setDK(0x0060)], # Dead Key Accent: Grave
    C("Alt-6"):         [getDK(),UC(0x02C6),C("Shift-Left"),setDK(0x02C6)], # Dead Key Accent: Circumflex
    C("Alt-W"):         [getDK(),UC(0x02D9),C("Shift-Left"),setDK(0x02D9)], # Dead Key Accent: Dot Above
    C("Alt-E"):         [getDK(),UC(0x00B4),C("Shift-Left"),setDK(0x00B4)], # Dead Key Accent: Acute

    # C("Shift-Alt-Y"):   [getDK(),UC(0x030F),C("Shift-Left"),setDK(0x030F)], # Dead Key Accent: Combining Double Grave
    # Double Grave accent acts odd when using the Combining Double Grave {U+030F}
    # Substituting {U+02F5}: ˵ Modifier Letter Middle Double Grave Accent
    C("Shift-Alt-Y"):   [getDK(),UC(0x02F5),C("Shift-Left"),setDK(0x02F5)], # Dead Key Accent: Double Grave (substitute)

    C("Alt-U"):         [getDK(),UC(0x00A8),C("Shift-Left"),setDK(0x00A8)], # Dead Key Accent: Umlaut
    C("Alt-I"):         [getDK(),UC(0x02BC),C("Shift-Left"),setDK(0x02BC)], # Dead Key Accent: Apostrophe/Horn
    C("Alt-P"):         [getDK(),UC(0x002C),C("Shift-Left"),setDK(0x002C)], # Dead Key Accent: Comma Below
    C("Alt-A"):         [getDK(),UC(0x00AF),C("Shift-Left"),setDK(0x00AF)], # Dead Key Accent: Macron/Line Above

    # C("Shift-Alt-S"):   [getDK(),UC(0x0311),C("Shift-Left"),setDK(0x0311)], # Dead Key Accent: Combining Inverted Breve
    C("Shift-Alt-S"):   [getDK(),UC(0x1D16),C("Shift-Left"),setDK(0x1D16)], # Dead Key Accent: Combining Inverted Breve

    # C("Shift-Alt-F"):   [getDK(),UC(0x0330),C("Shift-Left"),setDK(0x0330)], # Dead Key Accent: Combining Tilde Below
    # Tilde Below accent acts odd when using the Combining Tilde Below {U+0330}
    # Substituting {U+02F7}: ˷ Modifier Letter Low Tilde
    C("Shift-Alt-F"):   [getDK(),UC(0x02F7),C("Shift-Left"),setDK(0x02F7)], # Dead Key Accent: Tilde Below
    C("Shift-Alt-G"):   [getDK(),UC(0x2038),C("Shift-Left"),setDK(0x2038)], # Dead Key Accent: Caret/Circumflex Below

    C("Alt-H"):         [getDK(),UC(0x02CD),C("Shift-Left"),setDK(0x02CD)], # Dead Key Accent: Low Macron/Line Below
    C("Alt-J"):         [getDK(),UC(0x02DD),C("Shift-Left"),setDK(0x02DD)], # Dead Key Accent: Double Acute
    C("Alt-K"):         [getDK(),UC(0x02DA),C("Shift-Left"),setDK(0x02DA)], # Dead Key Accent: Ring Above
    C("Alt-L"):         [getDK(),UC(0x002D),C("Shift-Left"),setDK(0x002D)], # Dead Key Accent: Stroke/Hyphen-Minus

    C("Shift-Alt-Semicolon"): [getDK(),UC(0x2116),C("Shift-Left"),setDK(0x2116)], # Dead Key Accent: Numero Sign

    C("Alt-Z"):         [getDK(),UC(0x02C0),C("Shift-Left"),setDK(0x02C0)], # Dead Key Accent: Hook Above/Glottal Stop
    C("Alt-X"):         [getDK(),UC(0x002E),C("Shift-Left"),setDK(0x002E)], # Dead Key Accent: Dot Below
    C("Alt-C"):         [getDK(),UC(0x00B8),C("Shift-Left"),setDK(0x00B8)], # Dead Key Accent: Cedilla/Cedille
    C("Alt-V"):         [getDK(),UC(0x02C7),C("Shift-Left"),setDK(0x02C7)], # Dead Key Accent: Caron/hacek
    C("Alt-B"):         [getDK(),UC(0x02D8),C("Shift-Left"),setDK(0x02D8)], # Dead Key Accent: Breve
    C("Alt-N"):         [getDK(),UC(0x02DC),C("Shift-Left"),setDK(0x02DC)], # Dead Key Accent: Tilde
    C("Alt-M"):         [getDK(),UC(0x02DB),C("Shift-Left"),setDK(0x02DB)], # Dead Key Accent: Ogonek

    C("Shift-Alt-Dot"): [getDK(),UC(0x0294),C("Shift-Left"),setDK(0x0294)], # Dead Key Accent: Hook

}, when = lambda _: ac_Chr in deadkeys_list and _optspec_ABC is True)

keymap("Escape actions for dead keys", {
    # special case shortcuts that should cancel dead keys
    C("Esc"):           [getDK(),setDK(None)],                              # Leave accent char if dead keys Escaped
    C("Space"):         [getDK(),setDK(None)],                              # Leave accent char if user hits Space
    C("Delete"):        [getDK(),setDK(None)],                              # Leave accent char if user hits Delete
    C("Backspace"):     [getDK(),C("Backspace"),setDK(None)],               # Delete character if user hits Backspace
    C("Tab"):           [getDK(),C("Tab"),setDK(None)],                     # Leave accent char, insert Tab
    C("Enter"):         [getDK(),C("Enter"),setDK(None)],                   # Leave accent char, Enter key
    C("Up"):            [getDK(),C("Up"),setDK(None)],                      # Leave accent char, up arrow
    C("Down"):          [getDK(),C("Down"),setDK(None)],                    # Leave accent char, down arrow
    C("Left"):          [getDK(),C("Left"),setDK(None)],                    # Leave accent char, left arrow
    C("Right"):         [getDK(),C("Right"),setDK(None)],                   # Leave accent char, right arrow
    C("RC-Tab"):        [getDK(),bind,C("Alt-Tab"),setDK(None)],            # Leave accent char, task switch
    C("Shift-RC-Tab"):  [getDK(),bind,C("Shift-Alt-Tab"),setDK(None)],      # Leave accent char, task switch (reverse)
    C("RC-Grave"):      [getDK(),bind,C("Alt-Grave"),setDK(None)],          # Leave accent char, in-app window switch
    C("Shift-RC-Tab"):  [getDK(),bind,C("Shift-Alt-Grave"),setDK(None)],    # Leave accent char, in-app window switch (reverse)

    # common shortcuts that should also cancel dead keys
    C("RC-a"):                  [getDK(),C("RC-a"),setDK(None)],            # Leave accent char, select all
    C("RC-z"):                  [getDK(),C("RC-z"),setDK(None)],            # Leave accent char, undo
    C("RC-x"):                  [getDK(),C("RC-x"),setDK(None)],            # Leave accent char, cut
    C("RC-c"):                  [getDK(),C("RC-c"),setDK(None)],            # Leave accent char, copy
    C("RC-v"):                  [getDK(),C("RC-v"),setDK(None)],            # Leave accent char, paste

    ###  activate other dead keys correctly while one is active

    # US layout dead keys
    C("Alt-Grave"):     [getDK(),UC(0x0060),C("Shift-Left"),setDK(0x0060)], # Dead Key Accent: Grave
    C("Alt-E"):         [getDK(),UC(0x00B4),C("Shift-Left"),setDK(0x00B4)], # Dead Key Accent: Acute
    C("Alt-U"):         [getDK(),UC(0x00A8),C("Shift-Left"),setDK(0x00A8)], # Dead Key Accent: Umlaut
    C("Alt-I"):         [getDK(),UC(0x02C6),C("Shift-Left"),setDK(0x02C6)], # Dead Key Accent: Circumflex
    C("Alt-N"):         [getDK(),UC(0x02DC),C("Shift-Left"),setDK(0x02DC)], # Dead Key Accent: Tilde

    # ABC Extended layout dead keys (not here, see keymap above)


    # cancel dead keys with number keys row
    C("Grave"):                 [getDK(),C("Grave"),setDK(None)],
    C("Key_1"):                 [getDK(),C("Key_1"),setDK(None)],
    C("Key_2"):                 [getDK(),C("Key_2"),setDK(None)],
    C("Key_3"):                 [getDK(),C("Key_3"),setDK(None)],
    C("Key_4"):                 [getDK(),C("Key_4"),setDK(None)],
    C("Key_5"):                 [getDK(),C("Key_5"),setDK(None)],
    C("Key_6"):                 [getDK(),C("Key_6"),setDK(None)],
    C("Key_7"):                 [getDK(),C("Key_7"),setDK(None)],
    C("Key_8"):                 [getDK(),C("Key_8"),setDK(None)],
    C("Key_9"):                 [getDK(),C("Key_9"),setDK(None)],
    C("Key_0"):                 [getDK(),C("Key_0"),setDK(None)],
    C("Minus"):                 [getDK(),C("Minus"),setDK(None)],
    C("Equal"):                 [getDK(),C("Equal"),setDK(None)],
    C("Shift-Grave"):           [getDK(),C("Shift-Grave"),setDK(None)],
    C("Shift-Key_1"):           [getDK(),C("Shift-Key_1"),setDK(None)],
    C("Shift-Key_2"):           [getDK(),C("Shift-Key_2"),setDK(None)],
    C("Shift-Key_3"):           [getDK(),C("Shift-Key_3"),setDK(None)],
    C("Shift-Key_4"):           [getDK(),C("Shift-Key_4"),setDK(None)],
    C("Shift-Key_5"):           [getDK(),C("Shift-Key_5"),setDK(None)],
    C("Shift-Key_6"):           [getDK(),C("Shift-Key_6"),setDK(None)],
    C("Shift-Key_7"):           [getDK(),C("Shift-Key_7"),setDK(None)],
    C("Shift-Key_8"):           [getDK(),C("Shift-Key_8"),setDK(None)],
    C("Shift-Key_9"):           [getDK(),C("Shift-Key_9"),setDK(None)],
    C("Shift-Key_0"):           [getDK(),C("Shift-Key_0"),setDK(None)],
    C("Shift-Minus"):           [getDK(),C("Shift-Minus"),setDK(None)],
    C("Shift-Equal"):           [getDK(),C("Shift-Equal"),setDK(None)],

    # cancel dead keys with any letter on the keyboard that isn't supported by the dead key
    C("A"):                     [getDK(),C("A"),setDK(None)],
    C("B"):                     [getDK(),C("B"),setDK(None)],
    C("C"):                     [getDK(),C("C"),setDK(None)],
    C("D"):                     [getDK(),C("D"),setDK(None)],
    C("E"):                     [getDK(),C("E"),setDK(None)],
    C("F"):                     [getDK(),C("F"),setDK(None)],
    C("G"):                     [getDK(),C("G"),setDK(None)],
    C("H"):                     [getDK(),C("H"),setDK(None)],
    C("I"):                     [getDK(),C("I"),setDK(None)],
    C("J"):                     [getDK(),C("J"),setDK(None)],
    C("K"):                     [getDK(),C("K"),setDK(None)],
    C("L"):                     [getDK(),C("L"),setDK(None)],
    C("M"):                     [getDK(),C("M"),setDK(None)],
    C("N"):                     [getDK(),C("N"),setDK(None)],
    C("O"):                     [getDK(),C("O"),setDK(None)],
    C("P"):                     [getDK(),C("P"),setDK(None)],
    C("Q"):                     [getDK(),C("Q"),setDK(None)],
    C("R"):                     [getDK(),C("R"),setDK(None)],
    C("S"):                     [getDK(),C("S"),setDK(None)],
    C("T"):                     [getDK(),C("T"),setDK(None)],
    C("U"):                     [getDK(),C("U"),setDK(None)],
    C("V"):                     [getDK(),C("V"),setDK(None)],
    C("W"):                     [getDK(),C("W"),setDK(None)],
    C("X"):                     [getDK(),C("X"),setDK(None)],
    C("Y"):                     [getDK(),C("Y"),setDK(None)],
    C("Z"):                     [getDK(),C("Z"),setDK(None)],
    C("Shift-A"):               [getDK(),C("Shift-A"),setDK(None)],
    C("Shift-B"):               [getDK(),C("Shift-B"),setDK(None)],
    C("Shift-C"):               [getDK(),C("Shift-C"),setDK(None)],
    C("Shift-D"):               [getDK(),C("Shift-D"),setDK(None)],
    C("Shift-E"):               [getDK(),C("Shift-E"),setDK(None)],
    C("Shift-F"):               [getDK(),C("Shift-F"),setDK(None)],
    C("Shift-G"):               [getDK(),C("Shift-G"),setDK(None)],
    C("Shift-H"):               [getDK(),C("Shift-H"),setDK(None)],
    C("Shift-I"):               [getDK(),C("Shift-I"),setDK(None)],
    C("Shift-J"):               [getDK(),C("Shift-J"),setDK(None)],
    C("Shift-K"):               [getDK(),C("Shift-K"),setDK(None)],
    C("Shift-L"):               [getDK(),C("Shift-L"),setDK(None)],
    C("Shift-M"):               [getDK(),C("Shift-M"),setDK(None)],
    C("Shift-N"):               [getDK(),C("Shift-N"),setDK(None)],
    C("Shift-O"):               [getDK(),C("Shift-O"),setDK(None)],
    C("Shift-P"):               [getDK(),C("Shift-P"),setDK(None)],
    C("Shift-Q"):               [getDK(),C("Shift-Q"),setDK(None)],
    C("Shift-R"):               [getDK(),C("Shift-R"),setDK(None)],
    C("Shift-S"):               [getDK(),C("Shift-S"),setDK(None)],
    C("Shift-T"):               [getDK(),C("Shift-T"),setDK(None)],
    C("Shift-U"):               [getDK(),C("Shift-U"),setDK(None)],
    C("Shift-V"):               [getDK(),C("Shift-V"),setDK(None)],
    C("Shift-W"):               [getDK(),C("Shift-W"),setDK(None)],
    C("Shift-X"):               [getDK(),C("Shift-X"),setDK(None)],
    C("Shift-Y"):               [getDK(),C("Shift-Y"),setDK(None)],
    C("Shift-Z"):               [getDK(),C("Shift-Z"),setDK(None)],

    # cancel dead keys with other punctuation keys
    C("Left_Brace"):            [getDK(),C("Left_Brace"),setDK(None)],
    C("Right_Brace"):           [getDK(),C("Right_Brace"),setDK(None)],
    C("Backslash"):             [getDK(),C("Backslash"),setDK(None)],
    C("Semicolon"):             [getDK(),C("Semicolon"),setDK(None)],
    C("Apostrophe"):            [getDK(),C("Apostrophe"),setDK(None)],
    C("Comma"):                 [getDK(),C("Comma"),setDK(None)],
    C("Dot"):                   [getDK(),C("Dot"),setDK(None)],
    C("Slash"):                 [getDK(),C("Slash"),setDK(None)],
    C("Shift-Left_Brace"):      [getDK(),C("Shift-Left_Brace"),setDK(None)],
    C("Shift-Right_Brace"):     [getDK(),C("Shift-Right_Brace"),setDK(None)],
    C("Shift-Backslash"):       [getDK(),C("Shift-Backslash"),setDK(None)],
    C("Shift-Semicolon"):       [getDK(),C("Shift-Semicolon"),setDK(None)],
    C("Shift-Apostrophe"):      [getDK(),C("Shift-Apostrophe"),setDK(None)],
    C("Shift-Comma"):           [getDK(),C("Shift-Comma"),setDK(None)],
    C("Shift-Dot"):             [getDK(),C("Shift-Dot"),setDK(None)],
    C("Shift-Slash"):           [getDK(),C("Shift-Slash"),setDK(None)],

}, when = lambda _: ac_Chr in deadkeys_list)
# }, when = lambda _: ac_Chr in deadkeys_US or ac_Chr in deadkeys_ABC)

keymap("Disable Dead Keys",{
    # Nothing needs to be here. Tripwire keymap to disable active dead keys keymap(s)
}, when = lambda _: setDK(None)())



##############################################################################
###                                                                        ###
###                                                                        ###
###       █████  ██████   ██████     ███    ███  █████  ██ ███    ██       ###
###      ██   ██ ██   ██ ██          ████  ████ ██   ██ ██ ████   ██       ###
###      ███████ ██████  ██          ██ ████ ██ ███████ ██ ██ ██  ██       ###
###      ██   ██ ██   ██ ██          ██  ██  ██ ██   ██ ██ ██  ██ ██       ###
###      ██   ██ ██████   ██████     ██      ██ ██   ██ ██ ██   ████       ###
###                                                                        ###
###                                                                        ###
##############################################################################
# Main keymap for special characters on the ABC Extended layout
keymap("OptSpecialChars - ABC", {

    # Number keys row with Option
    ######################################################
    C("Alt-Grave"):     [UC(0x0060),C("Shift-Left"),setDK(0x0060)],     # Dead Key Accent: Grave

    C("Alt-1"):                 UC(0x00A1),                     # ¡ Inverted Exclamation Mark
    C("Alt-2"):                 UC(0x2122),                     # ™ Trade Mark Sign Emoji
    C("Alt-3"):                 UC(0x00A3),                     # £ British Pound currency symbol
    C("Alt-4"):                 UC(0x00A2),                     # ¢ Cent currency symbol
    C("Alt-5"):                 UC(0x00A7),                     # § Section symbol

    C("Alt-6"):         [UC(0x02C6),C("Shift-Left"),setDK(0x02C6)],     # Dead Key Accent: Circumflex

    C("Alt-7"):                 UC(0x00B6),                     # ¶ Paragraph mark (Pilcrow) symbol
    C("Alt-8"):                 UC(0x2022),                     # • Bullet Point symbol (solid)
    C("Alt-9"):                 UC(0x00AA),                     # ª Feminine Ordinal Indicator
    C("Alt-0"):                 UC(0x00BA),                     # º Masculine Ordinal Indicator
    C("Alt-Minus"):             UC(0x2013),                     # – En Dash punctuation mark
    C("Alt-Equal"):             UC(0x2260),                     # ≠ Not Equal To symbol

    # Number keys row with Shift+Option
    ######################################################
    C("Shift-Alt-Grave"):       UC(0x0300),                     # ` Combining Grave Accent
    C("Shift-Alt-1"):           UC(0x2044),                     # ⁄ Fraction Slash
    C("Shift-Alt-2"):           UC(0x20AC),                     # € Euro currency symbol
    C("Shift-Alt-3"):           UC(0x2039),                     # ‹ Single Left-Pointing Angle Quotation mark
    C("Shift-Alt-4"):           UC(0x203A),                     # › Single Right-Pointing Angle Quotation mark
    C("Shift-Alt-5"):           UC(0x2020),                     # † Simple dagger (cross) symbol
    C("Shift-Alt-6"):           UC(0x0302),                     #  ̂ Combining Circumflex Accent
    C("Shift-Alt-7"):           UC(0x2021),                     # ‡ Double dagger (cross) symbol
    C("Shift-Alt-8"):           UC(0x00B0),                     # ° Degree Sign
    C("Shift-Alt-9"):           UC(0x00B7),                     # · Middle Dot (interpunct/middot)
    C("Shift-Alt-0"):           UC(0x201A),                     # ‚ Single low-9 quotation mark
    C("Shift-Alt-Minus"):       UC(0x2014),                     # — Em Dash punctuation mark
    C("Shift-Alt-Equal"):       UC(0x00B1),                     # ± Plus Minus mathematical symbol

    # Tab key row with Option
    ######################################################
    C("Alt-Q"):                 UC(0x0153),                     # œ Small oe (oethel) ligature

    C("Alt-W"):         [UC(0x02D9),C("Shift-Left"),setDK(0x02D9)],     # Dead Key Accent: Dot Above
    C("Alt-E"):         [UC(0x00B4),C("Shift-Left"),setDK(0x00B4)],     # Dead Key Accent: Acute

    C("Alt-R"):                 UC(0x00AE),                     # ® Registered Trade Mark Sign
    C("Alt-T"):                 UC(0x00FE),                     # þ Latin Small Letter Thorn
    C("Alt-Y"):                 UC(0x00A5),                     # ¥ Japanese Yen currency symbol

    C("Alt-U"):         [UC(0x00A8),C("Shift-Left"),setDK(0x00A8)],     # Dead Key Accent: Umlaut
    C("Alt-I"):         [UC(0x02BC),C("Shift-Left"),setDK(0x02BC)],     # Dead Key Accent: Apostrophe/Horn

    C("Alt-O"):                 UC(0x00F8),                     # ø Latin Small Letter o with Stroke

    C("Alt-P"):         [UC(0x002C),C("Shift-Left"),setDK(0x002C)],     # Dead Key Accent: Comma Below

    C("Alt-Left_Brace"):        UC(0x201C),                     # “ Left Double Quotation Mark
    C("Alt-Right_Brace"):       UC(0x2018),                     # ‘ Left Single Quotation Mark
    C("Alt-Backslash"):         UC(0x00AB),                     # « Left-Pointing Double Angle Quotation Mark

    # Tab key row with Shift+Option
    ######################################################
    C("Shift-Alt-Q"):           UC(0x0152),                     # Œ Capital OE (Oethel) ligature
    C("Shift-Alt-W"):           UC(0x0307),                     # ˙ Combining Dot Above
    C("Shift-Alt-E"):           UC(0x0301),                     #  ́ Combining Acute Accent
    C("Shift-Alt-R"):           UC(0x2030),                     # ‰ Per mille symbol (zero over zero-zero)
    C("Shift-Alt-T"):           UC(0x00DE),                     # Þ Latin Capital Letter Thorn

    # C("Shift-Alt-Y"):           UC(0x02F5), # UC(0x030F),       # ̏  Combining Double Grave Accent
    # Spacing issues when using Combining Double Grave {U+030F}
    # Substituting {U+02F5}: ˵ Modifier Letter Middle Double Grave Accent for initial presentation
    C("Shift-Alt-Y"):   [UC(0x02F5),C("Shift-Left"),setDK(0x02F5)],     # Dead Key Accent: Double Grave

    C("Shift-Alt-U"):           UC(0x0308),                     #  ̈ Combining Diaeresis/Umlaut
    C("Shift-Alt-I"):           UC(0x031B),                     # ̛ Combining Horn (Apostrophe)
    C("Shift-Alt-O"):           UC(0x00D8),                     # Ø Latin Capital Letter O with Stroke
    C("Shift-Alt-P"):           UC(0x0326),                     #  ̦ Combining Comma Below
    C("Shift-Alt-Left_Brace"):  UC(0x201D),                     # ” Right Double Quotation Mark
    C("Shift-Alt-Right_Brace"): UC(0x2019),                     # ’ Right Single Quotation Mark
    C("Shift-Alt-Backslash"):   UC(0x00BB),                     # » Right-Pointing Double Angle Quotation Mark

    # CapsLock key row with Option
    ######################################################

    C("Alt-A"):         [UC(0x00AF),C("Shift-Left"),setDK(0x00AF)],     # Dead Key Accent: Macron/Line Above

    C("Alt-S"):                 UC(0x00DF),                     # ß German Eszett/beta (Sharfes/Sharp S)
    C("Alt-D"):                 UC(0x00F0),                     # ð Latin Small Letter Eth
    C("Alt-F"):                 UC(0x0192),                     # ƒ Function/florin currency symbol
    C("Alt-G"):                 UC(0x00A9),                     # © Copyright Sign

    C("Alt-H"):         [UC(0x02CD),C("Shift-Left"),setDK(0x02CD)],     # Dead Key Accent: Low Macron/Line Below
    C("Alt-J"):         [UC(0x02DD),C("Shift-Left"),setDK(0x02DD)],     # Dead Key Accent: Double Acute
    C("Alt-K"):         [UC(0x02DA),C("Shift-Left"),setDK(0x02DA)],     # Dead Key Accent: Ring Above
    C("Alt-L"):         [UC(0x002D),C("Shift-Left"),setDK(0x002D)],     # Dead Key Accent: Stroke/Hyphen-Minus

    C("Alt-Semicolon"):         UC(0x2026),                     # … Horizontal ellipsis
    C("Alt-Apostrophe"):        UC(0x00E6),                     # æ Small ae ligature

    # CapsLock key row with Shift+Option
    ######################################################
    C("Shift-Alt-A"):           UC(0x0304),                     #  ̄ Combining Macron/Line Below

    # C("Shift-Alt-S"): [UC(0x0311),C("Shift-Left"),setDK(0x0311)],   # Dead Key Accent: Combining Inverted Breve
    # Combining Inverted Breve has spacing problems
    # Substituting {U+1D16}: ᴖ Latin Small Letter Top Half O
    C("Shift-Alt-S"):   [UC(0x1D16),C("Shift-Left"),setDK(0x1D16)],     # Dead Key Accent: Inverted Breve

    C("Shift-Alt-D"):           UC(0x00D0),                     # Ð Latin Capital Letter Eth

    # C("Shift-Alt-F"):   [UC(0x0330),C("Shift-Left"),setDK(0x0330)],     # Dead Key Accent: Tilde Below
    # Combining Tilde Below has spacing problems
    # Substituting {U+02F7}: ˷ Modifier Letter Low Tilde
    C("Shift-Alt-F"):   [UC(0x02F7),C("Shift-Left"),setDK(0x02F7)],     # Dead Key Accent: Tilde Below
    C("Shift-Alt-G"):   [UC(0x2038),C("Shift-Left"),setDK(0x2038)],     # Dead Key Accent: Caret/Circumflex Below

    C("Shift-Alt-H"):           UC(0x0331),                     # ̱  Combining Macron/Line Below
    C("Shift-Alt-J"):           UC(0x030B),                     #  ̋ Combining Double Acute Accent
    C("Shift-Alt-K"):           UC(0x030A),                     #  ̊ Combining Ring Above
    C("Shift-Alt-L"):           UC(0x0335),                     #  ̵ Combining Short Stroke Overlay

    C("Shift-Alt-Semicolon"):  [UC(0x2116),C("Shift-Left"),setDK(0x2116)],      # Dead Key Accent: Numero Sign

    C("Shift-Alt-Apostrophe"):  UC(0x00C6),                     # Æ Capital AE ligature

    # Shift keys row with Option
    ######################################################

    C("Alt-Z"): [UC(0x02C0),C("Shift-Left"),setDK(0x02C0)],     # Dead Key Accent: Hook Above/Glottal Stop
    C("Alt-X"): [UC(0x002E),C("Shift-Left"),setDK(0x002E)],     # Dead Key Accent: Dot Below
    C("Alt-C"): [UC(0x00B8),C("Shift-Left"),setDK(0x00B8)],     # Dead Key Accent: Cedilla/Cedille
    C("Alt-V"): [UC(0x02C7),C("Shift-Left"),setDK(0x02C7)],     # Dead Key Accent: Caron/hacek
    C("Alt-B"): [UC(0x02D8),C("Shift-Left"),setDK(0x02D8)],     # Dead Key Accent: Breve
    C("Alt-N"): [UC(0x02DC),C("Shift-Left"),setDK(0x02DC)],     # Dead Key Accent: Tilde
    C("Alt-M"): [UC(0x02DB),C("Shift-Left"),setDK(0x02DB)],     # Dead Key Accent: Ogonek

    C("Alt-Comma"):             UC(0x2264),                     # ≤ Less Than or Equal To symbol
    C("Alt-Dot"):               UC(0x2265),                     # ≥ Greater Than or Equal To symbol
    C("Alt-Slash"):             UC(0x00F7),                     # ÷ Obelus/Division symbol

    # Shift keys row with Shift+Option
    ######################################################
    C("Shift-Alt-Z"):           UC(0x0309),                     # ̉  Combining Hook Above (hoi)
    C("Shift-Alt-X"):           UC(0x0323),                     # ̣  Combining Dot Below (nang)
    C("Shift-Alt-C"):           UC(0x0327),                     #  ̧ Combining Cedilla
    C("Shift-Alt-V"):           UC(0x030C),                     #  ̌ Combining Caron/hacek
    C("Shift-Alt-B"):           UC(0x0306),                     #  ̆ Combining Breve
    C("Shift-Alt-N"):           UC(0x0303),                     #  ̃ Combining Tilde
    C("Shift-Alt-M"):           UC(0x0328),                     #  ̨ Combining Ogonek (nasal hook)
    C("Shift-Alt-Comma"):       UC(0x201E),                     # „ Double Low-9 Quotation Mark

    C("Shift-Alt-Dot"): [UC(0x0294),C("Shift-Left"),setDK(0x0294)],     # Dead Key Accent: Hook

    C("Shift-Alt-Slash"):       UC(0x00BF),                     # ¿ Inverted Question mark

}, when = lambda ctx: ctx.wm_class.casefold() not in terminals and _optspec_ABC is True and _optspec_US is False)



######################################################################
###                                                                ###
###                                                                ###
###      ██    ██ ███████     ███    ███  █████  ██ ███    ██      ###
###      ██    ██ ██          ████  ████ ██   ██ ██ ████   ██      ###
###      ██    ██ ███████     ██ ████ ██ ███████ ██ ██ ██  ██      ###
###      ██    ██      ██     ██  ██  ██ ██   ██ ██ ██  ██ ██      ###
###       ██████  ███████     ██      ██ ██   ██ ██ ██   ████      ###
###                                                                ###
###                                                                ###
######################################################################
# Main keymap for special characters on the standard US layout
keymap("OptSpecialChars - US", {

    # Number keys row with Option
    ######################################################
    C("Alt-Grave"): [UC(0x0060), C("Shift-Left"), setDK(0x0060)],       # Dead Key Accent: Grave

    C("Alt-1"):                 UC(0x00A1),                     # ¡ Inverted Exclamation Mark
    C("Alt-2"):                 UC(0x2122),                     # ™ Trade Mark Sign Emoji
    C("Alt-3"):                 UC(0x00A3),                     # £ British Pound currency symbol
    C("Alt-4"):                 UC(0x00A2),                     # ¢ Cent currency symbol
    C("Alt-5"):                 UC(0x221E),                     # ∞ Infinity mathematical symbol
    C("Alt-6"):                 UC(0x00A7),                     # § Section symbol
    C("Alt-7"):                 UC(0x00B6),                     # ¶ Paragraph mark (Pilcrow) symbol
    C("Alt-8"):                 UC(0x2022),                     # • Bullet Point symbol (solid)
    C("Alt-9"):                 UC(0x00AA),                     # ª Feminine Ordinal Indicator
    C("Alt-0"):                 UC(0x00BA),                     # º Masculine Ordinal Indicator
    C("Alt-Minus"):             UC(0x2013),                     # – En Dash punctuation mark
    C("Alt-Equal"):             UC(0x2260),                     # ≠ Not Equal To symbol

    # Number keys row with Shift+Option
    ######################################################
    C("Shift-Alt-Grave"):       UC(0x0060),                     # ` Grave Accent (non-combining)
    C("Shift-Alt-1"):           UC(0x2044),                     # ⁄ Fraction Slash
    C("Shift-Alt-2"):           UC(0x20AC),                     # € Euro currency symbol
    C("Shift-Alt-3"):           UC(0x2039),                     # ‹ Single Left-Pointing Angle Quotation mark
    C("Shift-Alt-4"):           UC(0x203A),                     # › Single Right-Pointing Angle Quotation mark
    C("Shift-Alt-5"):           UC(0xFB01),                     # ﬁ Latin Small Ligature Fi
    C("Shift-Alt-6"):           UC(0xFB02),                     # ﬂ Latin Small Ligature Fl
    C("Shift-Alt-7"):           UC(0x2021),                     # ‡ Double dagger (cross) symbol
    C("Shift-Alt-8"):           UC(0x00B0),                     # ° Degree Sign
    C("Shift-Alt-9"):           UC(0x00B7),                     # · Middle Dot (interpunct/middot)
    C("Shift-Alt-0"):           UC(0x201A),                     # ‚ Single low-9 quotation mark
    C("Shift-Alt-Minus"):       UC(0x2014),                     # — Em Dash punctuation mark
    C("Shift-Alt-Equal"):       UC(0x00B1),                     # ± Plus Minus mathematical symbol

    # Tab key row with Option
    ######################################################
    C("Alt-Q"):                 UC(0x0153),                     # œ Small oe (oethel) ligature
    C("Alt-W"):                 UC(0x2211),                     # ∑ N-Ary Summation (sigma) notation

    C("Alt-E"):         [UC(0x00B4), C("Shift-Left"), setDK(0x00B4)],   # Dead Key Accent: Acute

    C("Alt-R"):                 UC(0x00AE),                     # ® Registered Trade Mark Sign
    C("Alt-T"):                 UC(0x2020),                     # † Simple dagger (cross) symbol
    C("Alt-Y"):                 UC(0x00A5),                     # ¥ Japanese Yen currency symbol

    C("Alt-U"):         [UC(0x00A8), C("Shift-Left"), setDK(0x00A8)],   # Dead Key Accent: Umlaut

    C("Alt-I"):         [UC(0x02C6), C("Shift-Left"), setDK(0x02C6)],   # Dead Key Accent: Circumflex

    C("Alt-O"):                 UC(0x00F8),                     # ø Latin Small Letter o with Stroke
    C("Alt-P"):                 UC(0x03C0),                     # π Greek Small Letter Pi
    C("Alt-Left_Brace"):        UC(0x201C),                     # “ Left Double Quotation Mark
    C("Alt-Right_Brace"):       UC(0x2018),                     # ‘ Left Single Quotation Mark
    C("Alt-Backslash"):         UC(0x00AB),                     # « Left-Pointing Double Angle Quotation Mark

    # Tab key row with Shift+Option
    ######################################################
    C("Shift-Alt-Q"):           UC(0x0152),                     # Œ Capital OE (Oethel) ligature
    C("Shift-Alt-W"):           UC(0x201E),                     # „ Double Low-9 Quotation mark
    C("Shift-Alt-E"):           UC(0x00B4),                     # ´ Acute Accent diacritic (non-combining)
    C("Shift-Alt-R"):           UC(0x2030),                     # ‰ Per mille symbol (zero over zero-zero)
    C("Shift-Alt-T"):           UC(0x02C7),                     # ˇ Caron/hacek diacritic (non-combining)
    C("Shift-Alt-Y"):           UC(0x00C1),                     # Á Latin Capital Letter A with Acute
    C("Shift-Alt-U"):           UC(0x00A8),                     # ¨ Diaeresis/Umlaut (non-combining)
    C("Shift-Alt-I"):           UC(0x02C6),                     # ˆ Circumflex Accent (non-combining)
    C("Shift-Alt-O"):           UC(0x00D8),                     # Ø Latin Capital Letter O with Stroke
    C("Shift-Alt-P"):           UC(0x220F),                     # ∏ N-Ary Product mathematical symbol
    C("Shift-Alt-Left_Brace"):  UC(0x201D),                     # ” Right Double Quotation Mark
    C("Shift-Alt-Right_Brace"): UC(0x2019),                     # ’ Right Single Quotation Mark
    C("Shift-Alt-Backslash"):   UC(0x00BB),                     # » Right-Pointing Double Angle Quotation Mark

    # CapsLock key row with Option
    ######################################################
    C("Alt-A"):                 UC(0x00E5),                     # å Small Letter a with Ring Above
    C("Alt-S"):                 UC(0x00DF),                     # ß German Eszett/beta (Sharfes/Sharp S)
    C("Alt-D"):                 UC(0x2202),                     # ∂ Partial Differential
    C("Alt-F"):                 UC(0x0192),                     # ƒ Function/florin currency symbol
    C("Alt-G"):                 UC(0x00A9),                     # © Copyright Sign
    C("Alt-H"):                 UC(0x02D9),                     # ˙ Dot Above diacritic (non-combining)
    C("Alt-J"):                 UC(0x2206),                     # ∆ Increment, laplace operator symbol
    C("Alt-K"):                 UC(0x02DA),                     # ˚ Ring Above diacritic (non-combining)
    C("Alt-L"):                 UC(0x00AC),                     # ¬ Not Sign angled dash symbol
    C("Alt-Semicolon"):         UC(0x2026),                     # … Horizontal ellipsis
    C("Alt-Apostrophe"):        UC(0x00E6),                     # æ Small ae ligature

    # CapsLock key row with Shift+Option
    ######################################################
    C("Shift-Alt-A"):           UC(0x00C5),                     # Å Capital Letter A with Ring Above
    C("Shift-Alt-S"):           UC(0x00CD),                     # Í Latin Capital Letter I with Acute
    C("Shift-Alt-D"):           UC(0x00CE),                     # Î Latin Capital Letter I with Circumflex
    C("Shift-Alt-F"):           UC(0x00CF),                     # Ï Latin Capital Letter I with Diaeresis
    C("Shift-Alt-G"):           UC(0x02DD),                     # ˝ Double Acute Accent (non-combining)
    C("Shift-Alt-H"):           UC(0x00D3),                     # Ó Latin Capital Letter O with Acute
    C("Shift-Alt-J"):           UC(0x00D4),                     # Ô Latin Capital Letter O with Circumflex
    #########################################################################################################
    # The Apple logo is at {U+F8FF} in a Unicode Private Use Area. Only at that location in Mac fonts. 
    # Symbol exists at {U+F000} in Baskerville Old Face font. 
    C("Shift-Alt-K"):   [apple_logo_alert(),UC(0xF000)],        #  Apple logo [req's Baskerville Old Face font]
    C("Shift-Alt-L"):           UC(0x00D2),                     # Ò Latin Capital Letter O with Grave
    C("Shift-Alt-Semicolon"):   UC(0x00DA),                     # Ú Latin Capital Letter U with Acute
    C("Shift-Alt-Apostrophe"):  UC(0x00C6),                     # Æ Capital AE ligature

    # Shift keys row with Option
    ######################################################
    C("Alt-Z"):                 UC(0x03A9),                     # Ω Greek Capital Letter Omega
    C("Alt-X"):                 UC(0x2248),                     # ≈ Almost Equal To symbol
    C("Alt-C"):                 UC(0x00E7),                     # ç Small Letter c with Cedilla
    C("Alt-V"):                 UC(0x221A),                     # √ Square Root radical sign
    C("Alt-B"):                 UC(0x222B),                     # ∫ Integral mathematical symbol

    C("Alt-N"): [UC(0x02DC), C("Shift-Left"), setDK(0x02DC)],   # Dead Key Accent: Tilde

    C("Alt-M"):                 UC(0x00B5),                     # µ Micro (mu) symbol
    C("Alt-Comma"):             UC(0x2264),                     # ≤ Less Than or Equal To symbol
    C("Alt-Dot"):               UC(0x2265),                     # ≥ Greater Than or Equal To symbol
    C("Alt-Slash"):             UC(0x00F7),                     # ÷ Obelus/Division symbol

    # Shift keys row with Shift+Option
    ######################################################
    C("Shift-Alt-Z"):           UC(0x00B8),                     # ¸ Spacing Cedilla diacritic (non-combining)
    C("Shift-Alt-X"):           UC(0x02DB),                     # ˛ Ogonek diacritic (non-combining)
    C("Shift-Alt-C"):           UC(0x00C7),                     # Ç Capital Letter C with Cedilla
    C("Shift-Alt-V"):           UC(0x25CA),                     # ◊ Lozenge (diamond) shape symbol
    C("Shift-Alt-B"):           UC(0x0131),                     # ı Latin Small Letter Dotless i
    C("Shift-Alt-N"):           UC(0x02DC),                     # ˜ Small Tilde character
    C("Shift-Alt-M"):           UC(0x00C2),                     # Â Latin Capital Letter A with Circumflex
    C("Shift-Alt-Comma"):       UC(0x00AF),                     # ¯ Macron/overline/overbar (non-combining)
    C("Shift-Alt-Dot"):         UC(0x02D8),                     # ˘ Breve diacritic (non-combining)
    C("Shift-Alt-Slash"):       UC(0x00BF),                     # ¿ Inverted Question mark

}, when = lambda ctx: ctx.wm_class.casefold() not in terminals and _optspec_US is True and _optspec_ABC is False)
