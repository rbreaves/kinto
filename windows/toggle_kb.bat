@echo off

IF "%1"=="mac" goto mac
IF "%1"=="win" goto win

echo Not found.
goto commonexit

:win
perl -pi -e "s/(; )(.*)(; WinModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
perl -pi -e "s/^(?!;)(.*)(; MacModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk"
goto commonexit

:mac
perl -pi -e "s/(; )(.*)(; MacModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
perl -pi -e "s/^(?!;)(.*)(; WinModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk"
goto commonexit

:commonexit
exit