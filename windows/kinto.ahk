#SingleInstance force
#NoEnv
#Persistent

DetectHiddenWindows, On
Run, %A_ScriptDir%\detectUSB.ahk

; I_Icon = %A_ScriptDir%\assets\kinto-white.ico           ; MacModifiers
; IfExist, %I_Icon%                                       ; MacModifiers
; Menu, Tray, Icon, %I_Icon%,, 1                          ; MacModifiers
; Menu, Tray, Tip, Mac - Kinto                            ; MacModifiers

; I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; WinModifiers
; IfExist, %I_Icon%                                       ; WinModifiers
; Menu, Tray, Icon, %I_Icon%,, 1                          ; WinModifiers
; Menu, Tray, Tip, Windows - Kinto                        ; WinModifiers

; Set Tray menu
; Menu, Tray, Standard
Menu, Tray, NoStandard ; to remove default menu
Menu, Tray, Add, Set Windows Keyboard, winkb
Menu, Tray, Add, Set Apple Keyboard, mackb
Menu, Tray, Add, Suspend Kinto, tray_suspend
Menu, Tray, Add, Returns to Desktop, min
Menu, Tray, Add
Menu, Tray, Add, Close, Exit
Menu, Tray, Click, 1

winkb(){
    Run, %A_ScriptDir%\NoShell.vbs %A_ScriptDir%\toggle_kb.bat win, %A_ScriptDir%
}

mackb(){
    Run, %A_ScriptDir%\NoShell.vbs %A_ScriptDir%\toggle_kb.bat mac, %A_ScriptDir%
}

min(){
; Refocus last active Window
Send {LAlt down}{tab}{LAlt up}
}  

tray_suspend(){
    suspend toggle
    if (a_isSuspended = 1){
        menu, tray, check  , Suspend Kinto
        I_Icon = %A_ScriptDir%\assets\kinto-color-invert.ico
        Menu, Tray, Icon, %I_Icon%,, 1
        Menu, Tray, Tip, Suspended - Kinto
        IfWinExist, detectUSB.ahk
            WinClose
    }
    else{
        menu, tray, unCheck, Suspend Kinto
;         I_Icon = %A_ScriptDir%\assets\kinto-white.ico           ; MacModifiers
;         I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; WinModifiers
        Menu, Tray, Icon, %I_Icon%,,1
        Run, %A_ScriptDir%\detectUSB.ahk
    }
    ; Refocus last active Window
    Send {LAlt down}{tab}{LAlt up}
}

Exit() {
    IfWinExist, detectUSB.ahk
        WinClose

    ExitApp
}

OnMessage(0x219, "notify_change")
return

lastkb = ""

DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

notify_change(wParam, lParam, msg, hwnd) 
{
    global lastkb
    ; kbtype = % ComObjCreate("WScript.Shell").Exec("cscript /nologo usb.vbs").StdOut.ReadAll()
    DetectHiddenWindows On
    Run %ComSpec%,, Hide, pid
    WinWait ahk_pid %pid%
    DllCall("AttachConsole", "UInt", pid)
    WshShell := ComObjCreate("Wscript.Shell")
    exec := WshShell.Exec("cscript /nologo usb.vbs")
    kbtype := exec.StdOut.ReadAll()
    DllCall("FreeConsole")
    Process Close, %pid%
    if lastkb != %kbtype%
    {

        if InStr(kbtype, "Apple")
        {
            ; MsgBox, Apple
            Run, %A_ScriptDir%\NoShell.vbs %A_ScriptDir%\toggle_kb.bat mac, %A_ScriptDir%
        }
        else{
            ; MsgBox, Windows
            Run, %A_ScriptDir%\NoShell.vbs %A_ScriptDir%\toggle_kb.bat win, %A_ScriptDir%
        }
        ; MsgBox % kbtype
    }
    lastkb = %kbtype%
}

SetTitleMatchMode, 2

GroupAdd, terminals, ahk_exe ubuntu.exe
GroupAdd, terminals, ahk_exe ConEmu.exe
GroupAdd, terminals, ahk_exe ConEmu64.exe
GroupAdd, terminals, ahk_exe powershell.exe
GroupAdd, terminals, ahk_exe WindowsTerminal.exe
GroupAdd, terminals, ahk_exe Hyper.exe
GroupAdd, terminals, ahk_exe Cmd.exe
GroupAdd, terminals, ahk_exe Terminus.exe
GroupAdd, terminals, Fluent Terminal ahk_class ApplicationFrameWindow

GroupAdd, posix, ahk_exe ubuntu.exe
GroupAdd, posix, ahk_exe ConEmu.exe
GroupAdd, posix, ahk_exe ConEmu64.exe
GroupAdd, posix, ahk_exe Hyper.exe
GroupAdd, posix, ahk_exe mintty.exe
GroupAdd, posix, ahk_exe Terminus.exe
GroupAdd, posix, Fluent Terminal ahk_class ApplicationFrameWindow

GroupAdd, ConEmu, ahk_exe ConEmu.exe
GroupAdd, ConEmu, ahk_exe ConEmu64.exe
GroupAdd, ConEmu, ahk_exe WindowsTerminal.exe

GroupAdd, editors, ahk_exe sublime_text.exe
GroupAdd, editors, ahk_exe VSCodium.exe
GroupAdd, editors, ahk_exe Code.exe

GroupAdd, vscode, ahk_exe VSCodium.exe
GroupAdd, vscode, ahk_exe Code.exe

GroupAdd, vstudio, ahk_exe devenv.exe

; New AltTab and CtrlTab fix
*tab:: 
{
    ; Tertiary 
    if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P") = false) {
        ; Secondary
        ; Send {LCtrl down}{Secondary up}{tab}
;        Send {LCtrl down}{LWin up}{tab}               ; WinModifiers
;        Send {LCtrl down}{LAlt up}{tab}               ; MacModifiers
        KeyWait, tab
    ; Tertiary
    } else if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P")) {
        ; Secondary
        ; Send {LCtrl down}{Secondary up}{LShift down}{tab}
;        Send {LCtrl down}{LWin up}{LShift down}{tab}  ; WinModifiers
;        Send {LCtrl down}{LAlt up}{LShift down}{tab}  ; MacModifiers
        KeyWait, tab
    ; Primary
;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P") = false) {   ; WinModifiers
;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P") = false) {   ; MacModifiers
        Send {LAlt down}{tab}
        KeyWait, tab
    ; Primary
;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P")) { ; WinModifiers
;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) { ; MacModifiers
        Send {LAlt down}{LShift down}{tab}
        KeyWait, tab
    ; Secondary 
;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) = false {   ; WinModifiers
;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P") = false) {   ; MacModifiers
        return
    ; Secondary
;     } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) {   ; WinModifiers
;     } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P")) {   ; MacModifiers
        return
    } else {
        send {Blind}{tab}
    }
    return
}

tab::Send {tab}

+tab::Send {Shift down}{tab}{Shift up}

; Basic Remap
;
; Primary::LCtrl
; Secondary::LAlt
; Tertiary::LWin

; $LAlt::LCtrl   ; WinModifiers
; $RAlt::RCtrl   ; WinModifiers
; $LWin::LAlt    ; WinModifiers
; $LCtrl::LWin   ; WinModifiers

; $LWin::LCtrl   ; MacModifiers
; $RWin::RCtrl   ; MacModifiers
; $LCtrl::LWin   ; MacModifiers

; Hack to disable start menu on winkey
; Static
$LCtrl up::Send {Ctrl down}{LWin up}{Ctrl up}

; temporary hack to ensure keys don't get stuck
; impacts Alt-Tab fix
; Primary
; $LAlt up::Send {LWin up}{LAlt up}{LCtrl up} ; WinModifiers
; $LWin up::Send {LWin up}{LAlt up}{LCtrl up} ; MacModifiers

; Close Apps 
^q::Send !{F4}

; Emoji Panel
#^Space::Send {LWin down};{LWin up}

; Full Screenshot
^+3::Send {PrintScreen}

; Region Screenshot
^+4::Send #+{S}

; wordwise support
$^Left::Send {Home}
$^+Left::Send +{Home}
$^Right::Send {End}
$^+Right::Send +{End}
^Up::Send ^{Home}
^+Up::Send ^+{Home}
^Down::Send ^{End}
^+Down::Send ^+{End}
^Backspace::Send +{Home}{Delete}
!Backspace::Send ^{Backspace}
!Left::Send ^{Left}
!+Left::Send ^+{Left}
!Right::Send ^{Right}
!+Right::Send ^+{Right}

; Cmd+Space Alternative
^Space::Send ^{Esc}

; ; Sublime Text Remaps for VS Code
#IfWinActive ahk_group vscode                               ; ST2CODE
    ; Remap Ctrl+Shift to behave like macOS Sublimetext
    ; Will extend cursor to multiple lines
    #+Up::send ^!{Up}                                   ; ST2CODE
    #+Down::send ^!{Down}                               ; ST2CODE
    ; Remap Ctrl+Cmd+G to select all matches
    #^g::send ^+{L}                                     ; ST2CODE
#If                                                         ; ST2CODE

#IfWinActive ahk_exe sublime_text.exe
    ; Remap Ctrl+Shift to behave like macOS Sublimetext
    ; Will extend cursor to multiple lines
    #+Up::send {shift up}^!{Up}
    #+Down::send {shift up}^!{Down}

    ; Remap Ctrl+Cmd+G to select all matches
    #^g::send !{F3}
#If

#IfWinActive ahk_group terminals
    ; Copy
    ^c::
    SetKeyDelay -1
    Send {Blind}{LShift down}{c DownTemp}
    return

    ^c up::
    SetKeyDelay -1
    Send {Blind}{c Up}{LShift Up}
    return

    ; Sigints - interrupt
    $#c::Send {Ctrl down}c{Ctrl up}

    ; Paste
    ^v::
    If WinActive("ahk_group posix"){
        Send {Blind}{Shift down}v{Shift up}
    }
    else{
        Send {Blind}v
    }
    return
#If

#IfWinActive ahk_group posix
    ; Open/Close Tab for those that support it
    $^t::
    If not WinActive("ahk_group ConEmu"){
        Send {LCtrl down}{LShift down}t{LCtrl Up}{LShift Up}
    }
    else{
        Send ^t
    }
    return

    $^w::
    If not WinActive("ahk_group ConEmu"){
        Send {LCtrl down}{LShift down}w{LCtrl Up}{LShift Up}
    }
    else{
        Send ^w
    }
    return

    ; End of Line
    ^e::
    SetKeyDelay -1
    Send {Blind}{e DownTemp}
    return

    ^e up::
    SetKeyDelay -1
    Send {Blind}{e Up}
    return

    ; Beginning of Line
    ^a::
    SetKeyDelay -1
    Send {Blind}{a DownTemp}
    return

    ^a up::
    SetKeyDelay -1
    Send {Blind}{a Up}
    return

    ^l::Send clear{Enter}
    ; #l::return
    ; Clear Terminal and Scroll Buffer
    ^k::Send clear && printf '\e[3J'{Enter}
    ; Nano editor shortcuts
    #g::Send {LCtrl down}g{LCtrl Up}
    #k::Send {LCtrl down}k{LCtrl Up}
    #x::Send {LCtrl down}x{LCtrl Up}
    #o::Send {LCtrl down}o{LCtrl Up}
    #r::Send {LCtrl down}r{LCtrl Up}
    #w::Send {LCtrl down}w{LCtrl Up}
    #\::Send {LCtrl down}\{LCtrl Up}
    #u::Send {LCtrl down}u{LCtrl Up}
    #j::Send {LCtrl down}j{LCtrl Up}
    #t::Send {LCtrl down}t{LCtrl Up}
    #_::Send {LCtrl down}_{LCtrl Up}
    #z::Send {LCtrl down}z{LCtrl Up}
    #y::Send {LCtrl down}y{LCtrl Up}
    #v::Send {LCtrl down}v{LCtrl Up}
#If