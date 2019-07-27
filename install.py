import os, platform, sysconfig, sys

yellow = "\033[1;33m"
green = "\033[0;32m"
red = "\033[1;31m"
reset = "\033[0;0m"

platform_name = platform.system()
# print sysconfig.get_platform()

sys.stdout.write(yellow)
cloud = '\u2601'.decode('unicode-escape')
circle = '\u25CE'.decode('unicode-escape')
heart = '\u2765'.decode('unicode-escape')
# bang = '\u1F589'.decode('unicode-escape')
print "           K!nt" +  circle
sys.stdout.write(reset)
print " - F!x the damn keyb" + circle + "ard. - "

print
print " You are using: " + platform_name
