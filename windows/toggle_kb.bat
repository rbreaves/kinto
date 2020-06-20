@echo off

IF "%1"=="mac" goto mac
IF "%1"=="win" goto win

echo Not found.
goto commonexit

:win
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; WinModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; MacModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk"
goto commonexit

:mac
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; MacModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; WinModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk"
goto commonexit

:commonexit
exit