class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	CBOLD     = '\033[1m'
	CITALIC   = '\033[3m'
	CURL      = '\033[4m'
	CBLINK    = '\033[5m'
	CBLINK2   = '\033[6m'
	CSELECTED = '\033[7m'

	CBLACK  = '\033[30m'
	CRED    = '\033[31m'
	CGREEN  = '\033[32m'
	CYELLOW = '\033[33m'
	CBLUE   = '\033[34m'
	CVIOLET = '\033[35m'
	CBEIGE  = '\033[36m'
	CWHITE  = '\033[37m'

	CBLACKBG  = '\033[40m'
	CREDBG    = '\033[41m'
	CGREENBG  = '\033[42m'
	CYELLOWBG = '\033[43m'
	CBLUEBG   = '\033[44m'
	CVIOLETBG = '\033[45m'
	CBEIGEBG  = '\033[46m'
	CWHITEBG  = '\033[47m'

	CGREY    = '\033[90m'
	CRED2    = '\033[91m'
	CGREEN2  = '\033[92m'
	CYELLOW2 = '\033[93m'
	CBLUE2   = '\033[94m'
	CVIOLET2 = '\033[95m'
	CBEIGE2  = '\033[96m'
	CWHITE2  = '\033[97m'

	CGREYBG    = '\033[100m'
	CREDBG2    = '\033[101m'
	CGREENBG2  = '\033[102m'
	CYELLOWBG2 = '\033[103m'
	CBLUEBG2   = '\033[104m'
	CVIOLETBG2 = '\033[105m'
	CBEIGEBG2  = '\033[106m'
	CWHITEBG2  = '\033[107m'

def yn_choice(message, default='y'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if choices == 'Y/n' else ('y', 'yes')
    return choice.strip().lower() in values

yn_choices()
choices = input()
values = int(input())
