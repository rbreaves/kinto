@echo off

IF "%1"=="mac" goto mac
IF "%1"=="win" goto win
IF "%1"=="chrome" goto chrome
IF "%1"=="ibm" goto ibm
IF "%1"=="auto" goto auto

echo Not found.
goto commonexit

:auto
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(;)( )(.*)(; Autodetect)|^(?!; )(.*)(; )(Autodetect)/$6$5$6$7$3$4/g" "%userprofile%\.kinto\kinto.ahk"
"%userprofile%\.kinto\kinto-start.vbs"
goto commonexit

:win
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; WinModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; Default)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; MacModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; CB\/IBM)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; Chromebook)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; IBM)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(ahk\"\" )(\w*)/$1win/gm" "%userprofile%\.kinto\kinto-start.vbs"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk" win
goto commonexit

:mac
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; MacModifiers)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; Default)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; WinModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; CB\/IBM)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; Chromebook)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; IBM)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(ahk\"\" )(\w*)/$1mac/gm" "%userprofile%\.kinto\kinto-start.vbs"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk" mac
goto commonexit

:chrome
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!; )(.*)(; Autodetect)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; WinModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; MacModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; Default)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; Chromebook)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; WinModifiers\/CB)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; CB\/IBM)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(ahk\"\" )(\w*)/$1chrome/gm" "%userprofile%\.kinto\kinto-start.vbs"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk" chrome
goto commonexit

:ibm
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!; )(.*)(; Autodetect)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; WinModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; Chromebook)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; MacModifiers)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/^(?!;)(.*)(; Default)/; $1$2/gm" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; IBM)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; WinModifiers\/CB\/IBM)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(; )(.*)(; CB\/IBM)/$2$3/g" "%userprofile%\.kinto\kinto.ahk"
C:\Strawberry\perl\bin\perl.exe -pi -e "s/(ahk\"\" )(\w*)/$1ibm/gm" "%userprofile%\.kinto\kinto-start.vbs"
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%userprofile%\.kinto\kinto.ahk" ibm
goto commonexit

:commonexit
exit