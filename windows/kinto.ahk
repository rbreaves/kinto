#SingleInstance force
#NoEnv
#Persistent

; DetectHiddenWindows, On           ; Autodetect
; Run, %A_ScriptDir%\detectUSB.ahk  ; Autodetect

; Enable Left clicks on Kinto Icon
; https://www.autohotkey.com/boards/viewtopic.php?t=9501
OnMessage(0x404, "AHK_NOTIFYICON")

AHK_NOTIFYICON(wParam, lParam)
{
    if (lParam = 0x202) { ; user left-clicked tray icon
        ;ADD ANY SUBROUTINE OR FUNCTION HERE
        Menu, Tray, Show
        return
    }
    else if (lParam = 0x203) { ; user double left-clicked tray icon
        ;ADD ANY SUBROUTINE OR FUNCTION HERE
        Menu, Tray, Show
        return
    }
}
; End Enable Left clicks

; I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; MacModifiers
; IfExist, %I_Icon%                                       ; MacModifiers
; Menu, Tray, Icon, %I_Icon%,, 1                          ; MacModifiers
; Menu, Tray, Tip, Mac - Kinto                            ; MacModifiers

; I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; WinModifiers/CB/IBM
; IfExist, %I_Icon%                                       ; WinModifiers/CB/IBM
; Menu, Tray, Icon, %I_Icon%,, 1                          ; WinModifiers/CB/IBM
; Menu, Tray, Tip, Windows - Kinto                        ; WinModifiers
; Menu, Tray, Tip, Chromebook - Kinto                     ; Chromebook
; Menu, Tray, Tip, IBM - Kinto                            ; IBM

Menu, Keyboards, Add, Windows, winkb
Menu, Keyboards, Add, Apple, mackb
Menu, Keyboards, Add, Chromebook, chromekb
Menu, Keyboards, Add, IBM (No Super/Win key), ibmkb

paramkb=%1%

if paramkb = mac
    checkKB = Apple
if paramkb = win
    checkKB = Windows
if paramkb = chrome
    checkKB = Chromebook
if paramkb = ibm
    checkKB = IBM (No Super/Win key)

menu, Keyboards, check, %checkKB%

; Set Tray menu
; Menu, Tray, Standard
Menu, Tray, NoStandard ; to remove default menu
Menu, Tray, Add, Keyboard Types, :Keyboards
Menu, Tray, Add, Autodetect Keyboards, autodetect
; Menu, Tray, check, Autodetect Keyboards ; Autodetect
; Menu, Tray, disable, Autodetect Keyboards ; CB/IBM
Menu, Tray, Add, Suspend Kinto, tray_suspend
; Add tray menu item for toggling Option key special character entry scheme
Menu, Tray, Add, OptSpecialChars   Shift+Opt+Cmd+O, toggle_optspecialchars
; Menu, Tray, Add, Returns to Desktop, min
Menu, Tray, Add
Menu, Tray, Add, Close, Exit
Menu, Tray, Click, 1

winkb(){
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" win, "%A_ScriptDir%"
}

mackb(){
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" mac, "%A_ScriptDir%"
}

chromekb(){
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" chrome, "%A_ScriptDir%"
}

ibmkb(){
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" ibm, "%A_ScriptDir%"
}

autodetect(){
    IfWinExist, detectUSB.ahk
        WinClose
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" auto, "%A_ScriptDir%"
}

min(){
; Refocus last active Window
Send {LAlt down}{tab}{LAlt up}
}  

tray_suspend(){
    suspend toggle
    if (a_isSuspended = 1){
        Gosub ReleaseModifiers
        menu, tray, check  , Suspend Kinto
        I_Icon = %A_ScriptDir%\assets\kinto-white.ico
        Menu, Tray, Icon, %I_Icon%,, 1
        Menu, Tray, Tip, Suspended - Kinto
        IfWinExist, detectUSB.ahk
            WinClose
    }
    else{
        menu, tray, unCheck, Suspend Kinto
;         I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; MacModifiers
;         I_Icon = %A_ScriptDir%\assets\kinto-white-invert.ico    ; WinModifiers/CB/IBM
;         Menu, Tray, Tip, Mac - Kinto                            ; MacModifiers
;         Menu, Tray, Tip, Windows - Kinto                        ; WinModifiers
;         Menu, Tray, Tip, Chromebook - Kinto                     ; Chromebook
;         Menu, Tray, Tip, IBM - Kinto                            ; IBM
        Menu, Tray, Icon, %I_Icon%,,1
        Run, %A_ScriptDir%\detectUSB.ahk
    }
    ; Refocus last active Window
    Send {LAlt down}{tab}{LAlt up}
}

Exit() {
    Gosub ReleaseModifiers
    IfWinExist, detectUSB.ahk
        WinClose

    ExitApp
}

SetTitleMatchMode, 2

GroupAdd, terminals, ahk_exe ubuntu.exe
GroupAdd, terminals, ahk_exe ubuntu2004.exe
GroupAdd, terminals, ahk_exe ConEmu.exe
GroupAdd, terminals, ahk_exe ConEmu64.exe
GroupAdd, terminals, ahk_exe powershell.exe
GroupAdd, terminals, ahk_exe WindowsTerminal.exe
GroupAdd, terminals, ahk_exe Hyper.exe
GroupAdd, terminals, ahk_exe mintty.exe
GroupAdd, terminals, ahk_exe Cmd.exe
GroupAdd, terminals, ahk_exe box.exe
GroupAdd, terminals, ahk_exe Terminus.exe
GroupAdd, terminals, Fluent Terminal ahk_class ApplicationFrameWindow
GroupAdd, terminals, ahk_class Console_2_Main

GroupAdd, posix, ahk_exe ubuntu.exe
GroupAdd, posix, ahk_exe ubuntu2004.exe
GroupAdd, posix, ahk_exe ConEmu.exe
GroupAdd, posix, ahk_exe ConEmu64.exe
GroupAdd, posix, ahk_exe Hyper.exe
GroupAdd, posix, ahk_exe mintty.exe
GroupAdd, posix, ahk_exe Terminus.exe
GroupAdd, posix, Fluent Terminal ahk_class ApplicationFrameWindow
GroupAdd, posix, ahk_class Console_2_Main
GroupAdd, posix, ahk_exe WindowsTerminal.exe

GroupAdd, ConEmu, ahk_exe ConEmu.exe
GroupAdd, ConEmu, ahk_exe ConEmu64.exe

GroupAdd, ExcPaste, ahk_exe Cmd.exe
GroupAdd, ExcPaste, ahk_exe mintty.exe

GroupAdd, editors, ahk_exe sublime_text.exe
GroupAdd, editors, ahk_exe VSCodium.exe
GroupAdd, editors, ahk_exe Code.exe

GroupAdd, browsers, ahk_exe chrome.exe
GroupAdd, browsers, ahk_exe opera.exe
GroupAdd, browsers, ahk_exe firefox.exe
GroupAdd, browsers, ahk_exe msedge.exe

; Disable Key Remapping for Virtual Machines
; Disable for Remote desktop solutions too
GroupAdd, remotes, ahk_exe VirtualBoxVM.exe
GroupAdd, remotes, ahk_exe mstsc.exe
GroupAdd, remotes, ahk_exe msrdc.exe
GroupAdd, remotes, ahk_exe nxplayer.bin
GroupAdd, remotes, ahk_exe vmconnect.exe
GroupAdd, remotes, ahk_exe RemoteDesktopManagerFree.exe
GroupAdd, remotes, ahk_exe vncviewer.exe
GroupAdd, remotes, Remote Desktop ahk_class ApplicationFrameWindow

; Disabled Edge for now - no ability to close all instances
; GroupAdd, browsers, Microsoft Edge ahk_class ApplicationFrameWindow

GroupAdd, vscode, ahk_exe VSCodium.exe
GroupAdd, vscode, ahk_exe Code.exe

GroupAdd, vstudio, ahk_exe devenv.exe

GroupAdd, intellij, ahk_exe idea.exe
GroupAdd, intellij, ahk_exe idea64.exe

; SetCapsLockState, AlwaysOff ; CB/IBM

; Keyboards w/o media keys can use this Remap
; This will replace unneeded dedicated keys
; with most commonly used media keys
;
; Insert::SoundSet, +1, , mute  ; Toggles Speaker
; +Insert::Insert               ; Shift Insert maps to Insert
; Home::SoundSetWaveVolume, -10 ; Decrease volume
; PgUp::SoundSetWaveVolume, +10 ; Increase volume
; Delete::Send {Media_Prev}     ; Previous
; End::Send {Media_Play_Pause}  ; Pause/Play
; PgDn::Send {Media_Next}       ; Next

; Virtual Desktop Hack via TotalSpaces2 - macOS Remote Desktop
; Custom Bind Gestures in Windows
; Shift-F8 on Left Swipe
; Shift-F9 on Right Swipe
#IfWinActive ahk_exe nxplayer.bin
    +F8::Send !+-     ; macOS TotalSpaces2 - Space Left
    +F6::Send !+=     ; macOS TotalSpaces2 - Space Right
#If
; +F8::Send {LCtrl down}{LWin down}{left}{LCtrl up}{LWin up}  ; Comment out on host machine
; +F6::Send {LCtrl down}{LWin down}{right}{LCtrl up}{LWin up} ; Comment out on host machine

#IfWinNotActive ahk_group remotes
    ; wordwise support
    ^Up::Send ^{Home}
    ^+Up::Send ^+{Home}
    ^Down::Send ^{End}
    ^+Down::Send ^+{End}
    $^Backspace::Send +{Home}{Delete}
    !Backspace::Send ^{Backspace}
    !Left::Send ^{Left}
    !+Left::Send ^+{Left}
    !Right::Send ^{Right}
    !+Right::Send ^+{Right}
    $^Left::Send {Home}
    $^+Left::Send +{Home}
    $^Right::Send {End}
    $^+Right::Send +{End}
#If

#IfWinNotActive ahk_group remotes

    ; New AltTab and CtrlTab fix
    *tab:: 
    {
        ; Tertiary 
        if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P") = false) {
            ; Secondary
            ; Send {LCtrl down}{Secondary up}{tab}
    ;        Send {LCtrl down}{LWin up}{tab}               ; WinModifiers
    ;        Send {LCtrl down}{LAlt up}{tab}               ; MacModifiers
    ;        Send {LCtrl down}{CapsLock up}{tab}           ; CB/IBM
            KeyWait, tab
        ; Tertiary
        } else if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P")) {
            ; Secondary
            ; Send {LCtrl down}{Secondary up}{LShift down}{tab}
    ;        Send {LCtrl down}{LWin up}{LShift down}{tab}     ; WinModifiers/CB
    ;        Send {LCtrl down}{LAlt up}{LShift down}{tab}     ; MacModifiers
    ;        Send {LCtrl down}{CapsLock up}{LShift down}{tab} ; IBM
            KeyWait, tab
        ; Primary
    ;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P") = false) {   ; WinModifiers/CB/IBM
    ;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P") = false) {   ; MacModifiers
            Send {LAlt down}{tab}
            KeyWait, tab
        ; Primary
    ;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P")) { ; WinModifiers/CB/IBM
    ;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) { ; MacModifiers
            Send {LAlt down}{LShift down}{tab}
            KeyWait, tab
        ; Secondary 
    ;    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) = false {     ; WinModifiers/CB
    ;    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P") = false) {     ; MacModifiers
    ;    } else if (GetKeyState("CapsLock", "P") AND GetKeyState("LShift", "P")) = false { ; IBM
            return
        ; Secondary
    ;     } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) {     ; WinModifiers/CB
    ;     } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P")) {     ; MacModifiers
    ;     } else if (GetKeyState("CapsLock", "P") AND GetKeyState("LShift", "P")) { ; IBM
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

    ; $LAlt::LCtrl     ; CB/IBM
    ; $RAlt::RCtrl     ; IBM
    ; $RCtrl::RAlt     ; CB/IBM
    ; $CapsLock::LWin  ; IBM
    ; $LCtrl::LAlt     ; CB/IBM

    ; $LAlt::LCtrl   ; WinModifiers
    ; $RAlt::RCtrl   ; WinModifiers
    ; $RCtrl::RAlt   ; WinModifiers
    ; $LWin::LAlt    ; WinModifiers
    ; $LCtrl::LWin   ; WinModifiers

    ; $LWin::LCtrl   ; MacModifiers
    ; $RWin::RCtrl   ; MacModifiers
    ; $LCtrl::LWin   ; MacModifiers

    ; Hack to disable start menu on winkey
    ; Static - Does not apply to IBM or Chromebooks
    ; $LCtrl up::Send {Ctrl down}{LWin up}{Ctrl up}            ; Default
    ; LWin::return                                             ; Chromebook
    ; RWin::return                                             ; Chromebook
    ; RAlt::return                                             ; Chromebook

    ; Disable Win-Up/Down - interferes with Sublime text 3 multi-cursors
    #Down::return
    #Up::return

    ; temporary hack to ensure keys don't get stuck
    ; impacts Alt-Tab fix
    ; Primary
    ; $LAlt up::Send {LWin up}{LAlt up}{LCtrl up} ; WinModifiers
    ; $LWin up::Send {LWin up}{LAlt up}{LCtrl up} ; MacModifiers
    ; $LAlt up::Send {LWin up}{CapsLock up}{LAlt up}{LCtrl up} ; CB/IBM

    !Enter:: 
    {
        if (GetKeyState("RAlt", "P")) {
            Send {Insert}
        }
        else{
            Send {Alt down}{Enter}{Alt up}
        }
        Return 
    }

    ; Remap Alt+Esc to Break/Pause
    !Esc::SendInput, {Pause}

    ; Go up or down a page
    #IfWinNotActive ahk_group editors
        $!Down::Send {PgDn}
        $!Up::Send {PgUp}
    #If

    ; Close Apps 
    ^q::Send !{F4}

    ; Minimize specific Window
    ^m::WinMinimize, A

    ; Minimize all but Active Window
    !^m::
    WinGet, winid ,, A
    WinMinimizeAll
    WinActivate ahk_id %winid%
    return

    ; hide all instances of active Program
    ^h::
    WinGetClass, class, A
    WinGet, AllWindows, List
    loop %AllWindows% {
        WinGetClass, WinClass, % "ahk_id " AllWindows%A_Index%
        if(InStr(WinClass,class)){
            WinMinimize, % "ahk_id " AllWindows%A_Index%
        }
    }
    return

    ; hide all but active program
    !^h::
    WinGetClass, class, A
    WinMinimizeAll
    WinGet, AllWindows, List
    loop %AllWindows% {
        WinGetClass, WinClass, % "ahk_id " AllWindows%A_Index%
        if(InStr(WinClass,class)){
            WinRestore, % "ahk_id " AllWindows%A_Index%
        }
    }
    return

    ; Show Desktop
    ^F3::Send #d

    ; Emoji Panel
    ; #^Space::Send {LWin down};{LWin up} ; Default
    ; !^Space::Send {LWin down};{LWin up} ; CB/IBM

    ; Full Screenshot
    ^+3::Send {PrintScreen}

    ; Region Screenshot
    ^+4::Send #+{S}

    ; Open File Browser
    ; !^space::Send #e ; Default
    ; #^space::Send #e ; CB/IBM

    ; #if GetKeyState("LWin", "P") || GetKeyState("RAlt", "P") ; Chromebook
    ;     Space::Send ^{Esc}                                   ; Chromebook
    ;     0::Send #0                                           ; Chromebook
    ;     1::Send #1                                           ; Chromebook
    ;     2::Send #2                                           ; Chromebook
    ;     3::Send #3                                           ; Chromebook
    ;     4::Send #4                                           ; Chromebook
    ;     5::Send #5                                           ; Chromebook
    ;     6::Send #6                                           ; Chromebook
    ;     7::Send #7                                           ; Chromebook
    ;     8::Send #8                                           ; Chromebook
    ;     9::Send #9                                           ; Chromebook
    ;     -::Send #-                                           ; Chromebook
    ;     =::Send #=                                           ; Chromebook
    ;     `::Send #`                                           ; Chromebook
    ;     `;::Send #;                                          ; Chromebook
    ;     a::Send #a                                           ; Chromebook
    ;     b::Send #b                                           ; Chromebook
    ;     c::Send #c                                           ; Chromebook
    ;     d::Send #d                                           ; Chromebook
    ;     e::Send #e                                           ; Chromebook
    ;     f::Send #f                                           ; Chromebook
    ;     g::Send #g                                           ; Chromebook
    ;     h::Send #h                                           ; Chromebook
    ;     i::Send #i                                           ; Chromebook
    ;     j::Send #j                                           ; Chromebook
    ;     k::Send #k                                           ; Chromebook
    ;     l::Send #l                                           ; Chromebook
    ;     m::Send #m                                           ; Chromebook
    ;     n::Send #n                                           ; Chromebook
    ;     o::Send #o                                           ; Chromebook
    ;     p::Send #p                                           ; Chromebook
    ;     q::Send #q                                           ; Chromebook
    ;     r::Send #r                                           ; Chromebook
    ;     s::Send #s                                           ; Chromebook
    ;     t::Send #t                                           ; Chromebook
    ;     u::Send #u                                           ; Chromebook
    ;     v::Send #v                                           ; Chromebook
    ;     w::Send #w                                           ; Chromebook
    ;     x::Send #x                                           ; Chromebook
    ;     y::Send #y                                           ; Chromebook
    ;     z::Send #z                                           ; Chromebook
    ; #If                                                      ; Chromebook

    #If Not WinActive("ahk_group terminals") and Not WinActive("ahk_group remotes")
        ^.::Send {Esc}
        ; emacs style
        #n::Send {Down}
        #p::Send {Up}
        #f::Send {Right}
        #b::Send {Left}
        #a::Send {Home}
        #e::Send {End}
        #d::Send {Delete}
        #k::Send +{End}{Backspace}
    #If

    ; Cmd+Space Alternative
    $^Space::Send ^{Esc}

    #IfWinActive ahk_group intellij
        ; $#c::Send ^{c}                  ; Default - Sigints interrupt
        ; $!c::Send ^{c}                  ; CB/IBM
        ; General
        ^0::Send !{0}                   ;Open corresponding tool window
        ^1::Send !{1}                   ;Open corresponding tool window
        ^2::Send !{2}                   ;Open corresponding tool window
        ^3::Send !{3}                   ;Open corresponding tool window
        ^4::Send !{4}                   ;Open corresponding tool window
        ^5::Send !{5}                   ;Open corresponding tool window
        ^6::Send !{6}                   ;Open corresponding tool window
        ^7::Send !{7}                   ;Open corresponding tool window
        ^8::Send !{8}                   ;Open corresponding tool window
        ^9::Send !{9}                   ;Open corresponding tool window
        #`::Send ^`                     ;Quick switch current scheme
        ^,::Send ^!s                    ;Open Settings dialog
        ^;::Send ^!+s                   ;Open Project Structure dialog
        ; Debugging
        ^!r::Send {F9}                  ;Resume program
        ; Search/Replace
        ^g::Send {F3}                   ;Find next
        ^+F3::Send +{F3}                ;Find previous
        #g::Send !j                     ;Select next occurrence
        ^#g::Send ^!+j                  ;Select all occurrences
        #+g::Send !+j                   ;Unselect occurrence
        ; Editing
        ; #Space::Send ^{Space}           ; Default - Basic code completion
        ; !Space::Send ^{Space}           ; CB/IBM - Basic code completion
        #+Space::Send ^+{Space}         ;Smart code completion
        #j::Send ^q                     ;Quick documentation lookup
        ^n::Send !{Insert}              ;Generate code...
        #o::Send ^o                     ;Override methods
        #i::Send ^i                     ;Implement methods
        !Up::Send ^w                    ;Extend selection
        !Down::Send ^+w                 ;Shrink selection
        #+q::Send !q                    ;Context info
        #!o::Send ^!o                   ;Optimize imports
        #!i::Send ^!i                   ;Auto-indent line(s)
        $^Backspace::Send ^y            ;Delete line at caret
        #+j::Send ^+j                   ;Smart line join
        !Delete::Send ^{Delete}         ;Delete to word end
        !Backspace::Send ^{Backspace}   ;Delete to word start
        ^+::Send ^{NumpadAdd}           ;Expand code block
        ^-::Send ^{NumpadSub}           ;Collapse code block
        ^++::Send ^+{NumpadAdd}         ;Expand all
        ^+-::Send ^+{NumpadSub}         ;Collapse all
        ^w::Send ^{F4}                  ;Close active editor tab
        ; Refactoring
        ^Delete::Send !{Delete}         ;Safe Delete
        ^T::Send ^!+T                   ;Refactor this
        ; Navigation
        ^o::Send ^n                     ;Go to class
        ^+o::Send ^+n                   ;Go to file
        ^!o::Send ^!+n                  ;Go to symbol
        #Right::Send !{Right}           ;Go to next editor tab
        #Left::Send !{Left}             ;Go to previous editor tab
        #l::Send ^g                     ;Go to line
        #e::Send ^e                     ;Recent files popup
        ; !Space::Send ^+i                ; Default - Open quick definition lookup
        ; #Space::Send ^+i                ; CB/IBM - Open quick definition lookup
        ^Y::Send ^+i                    ;Open quick definition lookup
        #+b::Send ^+b                   ;Go to type declaration
        #Up::Send !{Up}                 ;Go to previous
        #Down::Send !{Down}             ;Go to next method
        #h::Send ^h                     ;Type hierarchy
        #!h::Send ^!h                   ;Call hierarchy
        ^Down::Send ^{Enter}            ;Edit source/View source
        !Home::Send !{Home}             ;Show navigation bar
        F2::Send {F11}                  ;Toggle bookmark
        #F3::Send ^{F11}                ;Toggle bookmark with mnemonic
        #0::Send ^{0}                   ;Go to numbered bookmark
        #1::Send ^{1}                   ;Go to numbered bookmark
        #2::Send ^{2}                   ;Go to numbered bookmark
        #3::Send ^{3}                   ;Go to numbered bookmark
        #4::Send ^{4}                   ;Go to numbered bookmark
        #5::Send ^{5}                   ;Go to numbered bookmark
        #6::Send ^{6}                   ;Go to numbered bookmark
        #7::Send ^{7}                   ;Go to numbered bookmark
        #8::Send ^{8}                   ;Go to numbered bookmark
        #9::Send ^{9}                   ;Go to numbered bookmark
        ^F3::Send +{F11}                ;Show bookmarks
        ; Compile and Run
        #!r::Send !+{F10}               ;Select configuration and run
        #!d::Send !+{F9}                ;Select configuration and debug
        #r::Send +{F10}                 ;Run
        #d::Send +{F9}                  ;Debug
        #+r::Send ^+{F10}               ;Run context configuration from editor
        #+d::Send ^+{F9}                ;Debug context configuration from editor
        ; VCS/Local History
        #v::Send !`                     ;VCS quick popup
    #If

    ; Close all browsers
    #IfWinActive ahk_group browsers
        ; Page Navigation
        ^[::send !{Left}                ; Go to prior page
        ^]::send !{Right}               ; Go to next page
         ;Tab Navigation
        ^+[::send ^{PgUp}               ; Go to prior tab (left)
        ^+]::send ^{PgDn}               ; Go to next tab (right)
        ^!Left::send ^{PgUp}            ; Go to prior tab (left)
        ^!Right::send ^{PgDn}           ; Go to next tab (right)
        #Left::send ^{PgUp}             ; Go to prior tab (left)
        #Right::send ^{PgDn}            ; Go to next tab (right)
        ^q::send {Alt Down}f{Alt Up}x   ; exit all windows
        ; Dev Tools
        !^i::send {Ctrl Down}{Shift Down}i{Shift Up}{Ctrl Up}
        !^j::send {Ctrl Down}{Shift Down}j{Shift Up}{Ctrl Up}
        ; Open preferences
        #IfWinActive ahk_exe firefox.exe
            ^,::send, {Ctrl Down}t{Ctrl Up}about:preferences{Enter}
            ^+n::send ^+p
        #If
        #IfWinActive ahk_exe chrome.exe
            ^,::send {Alt Down}e{Alt Up}s{Enter}
        #If
        #IfWinActive ahk_exe msedge.exe
            ^,::send {Alt Down}e{Alt Up}s{Enter}
        #If
        #IfWinActive ahk_exe opera.exe
            ^,::send {Ctrl Down}{F12}{Ctrl Up}
        #If
    #If

    ; Sublime Text Remaps for VS Code
    #IfWinActive ahk_group vscode
        #p::send {Up}                                        ; Allow for traversing quick list
        #n::send {Down}                                      ; Allow for traversing quick list
        ; Remap Ctrl+Shift to behave like macOS Sublimetext
        ; Will extend cursor to multiple lines
    ;    #+Up::send ^!{Up}                                   ; Default - ST2CODE
    ;    !+Up::send ^!{Up}                                   ; CB/IBM - ST2CODE
    ;    #+Down::send ^!{Down}                               ; Default - ST2CODE
    ;    !+Down::send ^!{Down}                               ; CB/IBM - ST2CODE
        ; Remap Ctrl+Cmd+G to select all matches
    ;    #^g::send ^+{L}                                     ; Default - ST2CODE
    ;    !^g::send ^+{L}                                     ; CB/IBM - ST2CODE
        !+g::send ^+{G}                                      ; View source control
    ;    $#c::Send {Ctrl down}c{Ctrl up}                     ; Default - Sigints interrupt
    ;    $!c::Send {Ctrl down}c{Ctrl up}                     ; CB/IBM
    ;    $#x::Send {Ctrl down}x{Ctrl up}                     ; Default - Sigints interrupt
    ;    $!x::Send {Ctrl down}x{Ctrl up}                     ; CB/IBM

    ;   #Space::Send ^{Space}                                ; Default - Basic code completion
    ;   !Space::Send ^{Space}                                ; CB/IBM - Basic code completion
    #If

    #IfWinActive ahk_exe sublime_text.exe
        ; #x::Send ^{x}                                           ; Default - Terminal - Ctrl-x
        ; #c::Send ^{c}                                           ; Default - Terminal - Ctrl-c sigint
        ; !x::Send ^{x}                                           ; CB/IBM
        ; !c::Send ^{c}                                           ; CB/IBM - Sigint
        ; #c::send ^{Pause}                                       ; cancel_build
        ; #Space::Send ^{Space}                                   ; Default - Basic code completion
        ; !Space::Send ^{Space}                                   ; CB/IBM - Basic code completion
        #^Up::send !{O}                                         ; Switch file
        #^f::send {F11}                                         ; toggle_full_screen
        ^!v::send {Ctrl Down}k{Ctrl Up}{Ctrl Down}v{Ctrl Up}    ; paste_from_history
        ^Up::Return                                             ; cancel scroll_lines up
        ^!Up::send ^{Up}                                        ; scroll_lines up
        ^Down::Return                                           ; cancel scroll_lines down
        ^!Down::send ^{Down}                                    ; scroll_lines down
        ; #+Up::send {shift up}^!{Up}                             ; Default - multi-cursor up
        ; #+Down::send {shift up}^!{Down}                         ; Default - multi-cursor down
        ; !+Up::send {shift up}^!{Up}                             ; CB/IBM - multi-cursor up
        ; !+Down::send {shift up}^!{Down}                         ; CB/IBM - multi-cursor down
        ^PgDn::Return                                           ; cancel next_view
        ^PgUp::Return                                           ; cancel prev_view
        ^+{::send ^{PgDn}                                       ; next_view
        ^+}::send ^{PgUp}                                       ; prev_view
        ^!Right::send ^{PgDn}                                   ; next_view
        ^!Left::send ^{PgUp}                                    ; prev_view
        Insert::Return                                          ; cancel toggle_overwrite
        ^!O::send {Insert}                                      ; toggle_overwrite
        ; !c::Return                                              ; Default - cancel toggle_case_sensitive
        ^!c::send !{c}                                          ; toggle_case_sensitive
        ; ^h::Return                                              ; cancel replace
        ^!f::send ^{h}                                          ; replace
        ^+h::Return                                             ; cancel replace_next
        ^!e::send ^+{h}                                         ; replace_next
        F3::Return                                              ; cancel find_next
        ^g::send {F3}                                           ; find_next
        #g::send ^{g}                                           ; goto line - disable game bar - Start menu -> Game bar shortcuts -> toggle Off
        *F3::Return                                             ; cancel find_prev, find_under, find_all_under
        ^+g::send +{F3}                                         ; find_prev
        #!g::send ^{F3}                                         ; find_under
        #!+g::send ^+{F3}                                       ; find_under_prev
        ; #^g::send !{F3}                                         ; Default - find_all_under
        ; !^g::send !{F3}                                         ; CB/IBM - find_all_under
        ^+Up::Return                                            ; cancel swap_line_up
        #!Up::send ^+{Up}                                       ; swap_line_up
        ^+Down::Return                                          ; cancel swap_line_down
        #!Down::send ^+{Down}                                   ; swap_line_down
        ^Pause::Return                                          ; cancel cancel_build
        ; #c::send ^{Pause}                                       ; cancel_build
        F9::Return                                              ; cancel sort_lines case_s false
        F5::send {F9}                                           ; sort_lines case_s false
        #F9::Return                                             ; cancel sort_lines case_s true
        #F5::send #{F9}                                         ; sort_lines case_s true
        !+1::Return                                             ; cancel set_layout
        ^!1::send !+1                                           ; set_layout
        !+2::Return                                             ; cancel set_layout
        ^!2::send !+2                                           ; set_layout
        !+3::Return                                             ; cancel set_layout
        ^!3::send !+3                                           ; set_layout
        !+4::Return                                             ; cancel set_layout
        ^!4::send !+4                                           ; set_layout
        !+5::Return                                             ; cancel set_layout
        ^!5::send !+5                                           ; set_layout
        !+8::Return                                             ; cancel set_layout
        ^!8::send !+8                                           ; set_layout
        !+9::Return                                             ; cancel set_layout
        ^!9::send !+9                                           ; set_layout
    #If

    #IfWinActive ahk_group terminals

        ; End of Line
        ; #e:: ; Default
        ; !e:: ; CB/IBM
        Send {End}
        return

        ; Beginning of Line
        ; #a:: ; Default
        ; !a:: ; CB/IBM
        Send {Home}
        return

        ; Copy
        ^c::
        If WinActive("ahk_exe cmd.exe") OR WinActive("ahk_exe box.exe"){
            Send {Enter}
        }
        else if WinActive("ahk_exe mintty.exe"){
            SetKeyDelay -1
            Send {Blind}{Insert}
        }
        ; else if WinActive("ahk_exe WindowsTerminal.exe"){ ; WinTerm
        ;     SetKeyDelay -1                                ; WinTerm
        ;     Send {Blind}{F13}                             ; WinTerm
        ; }                                                 ; WinTerm
        else{
            SetKeyDelay -1
            Send {Blind}{LShift down}{c DownTemp}
        }
        return

        ^c up::
        If not WinActive("ahk_group cmd.exe") OR WinActive("ahk_exe box.exe"){
            SetKeyDelay -1
            Send {Blind}{c Up}{LShift Up}
        }
        return

        ; Sigints - interrupt
        ; $#c::Send {Ctrl down}c{Ctrl up} ; Default
        ; $!c::Send {Ctrl down}c{Ctrl up} ; CB/IBM
        $^.::Send {Ctrl down}c{Ctrl up}

        ; Windows Terminal
        ; Ctrl+Shift+C should do nothing
        If WinActive("ahk_exe WindowsTerminal.exe"){
            $#+c::return
        }

        ; Paste
        $^v::
        If WinActive("ahk_exe mintty.exe"){
            Send {Shift down}{Insert}{Shift up}
        }
        else if WinActive("ahk_group posix"){
            Send {Blind}{Shift down}v{Shift up}
        }
        else if WinActive("ahk_exe box.exe"){
            SendEvent {RButton}
        }
        else{
            Send {Blind}v
        }
        return
    #If

    #IfWinActive ahk_group posix
        ; Open/Close Tab for those that support it
        $^t::
        If not WinActive("ahk_group ConEmu") AND not WinActive("ahk_class Console_2_Main"){
            Send {Blind}{LShift down}t{LShift Up}
        }
        else if WinActive("ahk_class Console_2_Main"){
            Send {Blind}{F1}{LShift Up}
        }
        else{
            Send {Blind}t
        }
        return


        $^w::
        If not WinActive("ahk_group ConEmu"){
            Send {Blind}{LShift down}w{LShift Up}
        }
        else{
            Send ^w
        }
        return

        ^l::Send clear{Enter}
        ; #l::return
        ; Clear Terminal and Scroll Buffer
        ^k::Send clear && printf '\e[3J'{Enter}
        ; Remap Physical Ctrl back to Ctrl
        ; #0::Send {LCtrl down}0{Ctrl up}  ; Default
        ; #1::Send {LCtrl down}1{Ctrl up}  ; Default
        ; #2::Send {LCtrl down}2{Ctrl up}  ; Default
        ; #3::Send {LCtrl down}3{Ctrl up}  ; Default
        ; #4::Send {LCtrl down}4{Ctrl up}  ; Default
        ; #5::Send {LCtrl down}5{Ctrl up}  ; Default
        ; #6::Send {LCtrl down}6{Ctrl up}  ; Default
        ; #7::Send {LCtrl down}7{Ctrl up}  ; Default
        ; #8::Send {LCtrl down}8{Ctrl up}  ; Default
        ; #9::Send {LCtrl down}9{Ctrl up}  ; Default
        ; #-::Send {LCtrl down}-{Ctrl up}  ; Default
        ; #=::Send {LCtrl down}={Ctrl up}  ; Default
        ; #`::Send {LCtrl down}`{Ctrl up}  ; Default
        ; #a::Send {LCtrl down}a{Ctrl up}  ; Default
        ; #b::Send {LCtrl down}b{Ctrl up}  ; Default
        ; #c::Send {LCtrl down}c{Ctrl up}  ; Default
        ; #d::Send {LCtrl down}d{Ctrl up}  ; Default
        ; #e::Send {LCtrl down}e{Ctrl up}  ; Default
        ; #f::Send {LCtrl down}f{Ctrl up}  ; Default
        ; #g::Send {LCtrl down}g{Ctrl up}  ; Default
        ; #h::Send {LCtrl down}h{Ctrl up}  ; Default
        ; #i::Send {LCtrl down}i{Ctrl up}  ; Default
        ; #j::Send {LCtrl down}j{Ctrl up}  ; Default
        ; #k::Send {LCtrl down}k{Ctrl up}  ; Default
        ; #l::Send {LCtrl down}l{Ctrl up}  ; Default
        ; #m::Send {LCtrl down}m{Ctrl up}  ; Default
        ; #n::Send {LCtrl down}n{Ctrl up}  ; Default
        ; #o::Send {LCtrl down}o{Ctrl up}  ; Default
        ; #p::Send {LCtrl down}p{Ctrl up}  ; Default
        ; #q::Send {LCtrl down}q{Ctrl up}  ; Default
        ; #r::Send {LCtrl down}r{Ctrl up}  ; Default
        ; #s::Send {LCtrl down}s{Ctrl up}  ; Default
        ; #t::Send {LCtrl down}t{Ctrl up}  ; Default
        ; #u::Send {LCtrl down}u{Ctrl up}  ; Default
        ; #v::Send {LCtrl down}v{Ctrl up}  ; Default
        ; #w::Send {LCtrl down}w{Ctrl up}  ; Default
        ; #x::Send {LCtrl down}x{Ctrl up}  ; Default
        ; #y::Send {LCtrl down}y{Ctrl up}  ; Default
        ; #z::Send {LCtrl down}z{Ctrl up}  ; Default
        ; !0::Send {LCtrl down}0{Ctrl up}  ; CB/IBM
        ; !1::Send {LCtrl down}1{Ctrl up}  ; CB/IBM
        ; !2::Send {LCtrl down}2{Ctrl up}  ; CB/IBM
        ; !3::Send {LCtrl down}3{Ctrl up}  ; CB/IBM
        ; !4::Send {LCtrl down}4{Ctrl up}  ; CB/IBM
        ; !5::Send {LCtrl down}5{Ctrl up}  ; CB/IBM
        ; !6::Send {LCtrl down}6{Ctrl up}  ; CB/IBM
        ; !7::Send {LCtrl down}7{Ctrl up}  ; CB/IBM
        ; !8::Send {LCtrl down}8{Ctrl up}  ; CB/IBM
        ; !9::Send {LCtrl down}9{Ctrl up}  ; CB/IBM
        ; !-::Send {LCtrl down}-{Ctrl up}  ; CB/IBM
        ; !=::Send {LCtrl down}={Ctrl up}  ; CB/IBM
        ; !`::Send {LCtrl down}`{Ctrl up}  ; CB/IBM
        ; !a::Send {LCtrl down}a{Ctrl up}  ; CB/IBM
        ; !b::Send {LCtrl down}b{Ctrl up}  ; CB/IBM
        ; !c::Send {LCtrl down}c{Ctrl up}  ; CB/IBM
        ; !d::Send {LCtrl down}d{Ctrl up}  ; CB/IBM
        ; !e::Send {LCtrl down}e{Ctrl up}  ; CB/IBM
        ; !f::Send {LCtrl down}f{Ctrl up}  ; CB/IBM
        ; !g::Send {LCtrl down}g{Ctrl up}  ; CB/IBM
        ; !h::Send {LCtrl down}h{Ctrl up}  ; CB/IBM
        ; !i::Send {LCtrl down}i{Ctrl up}  ; CB/IBM
        ; !j::Send {LCtrl down}j{Ctrl up}  ; CB/IBM
        ; !k::Send {LCtrl down}k{Ctrl up}  ; CB/IBM
        ; !l::Send {LCtrl down}l{Ctrl up}  ; CB/IBM
        ; !m::Send {LCtrl down}m{Ctrl up}  ; CB/IBM
        ; !n::Send {LCtrl down}n{Ctrl up}  ; CB/IBM
        ; !o::Send {LCtrl down}o{Ctrl up}  ; CB/IBM
        ; !p::Send {LCtrl down}p{Ctrl up}  ; CB/IBM
        ; !q::Send {LCtrl down}q{Ctrl up}  ; CB/IBM
        ; !r::Send {LCtrl down}r{Ctrl up}  ; CB/IBM
        ; !s::Send {LCtrl down}s{Ctrl up}  ; CB/IBM
        ; !t::Send {LCtrl down}t{Ctrl up}  ; CB/IBM
        ; !u::Send {LCtrl down}u{Ctrl up}  ; CB/IBM
        ; !v::Send {LCtrl down}v{Ctrl up}  ; CB/IBM
        ; !w::Send {LCtrl down}w{Ctrl up}  ; CB/IBM
        ; !x::Send {LCtrl down}x{Ctrl up}  ; CB/IBM
        ; !y::Send {LCtrl down}y{Ctrl up}  ; CB/IBM
        ; !z::Send {LCtrl down}z{Ctrl up}  ; CB/IBM
    #If
#If

ReleaseModifiers:
Send {RCtrl up}
Send {LCtrl up}
Send {RAlt up}
Send {LAlt up}
Send {RWin up}
Send {LWin up}
Send {RShift up}
Send {LShift up}
return

; ###############################################################################################################
; ###   Special character insertion like Apple/macOS Option key methods, mapping to Unicode input method
; ###   Common symbols available with Option+key or Shift+Option+key, accented keys with Option+Key1, then Key2
; ###############################################################################################################

; Shortcut to activate Option key special character scheme
^+!o::Gosub, toggle_optspecialchars

; Function (subroutine?) for activation by tray menu item or keyboard shortcut
toggle_optspecialchars:
    optspecialchars:=!optspecialchars         ; Toggle value of optspecialchars variable on/off
    if (optspecialchars = 1) {
        Menu, Tray, Check, OptSpecialChars   Shift+Opt+Cmd+O
        MsgBox, 0, ALERT, % "Option key special character entry scheme is now ENABLED.`n`n"
                            . "WARNING: This will interfere with many Alt and Alt-Shift shortcuts.`n`n"
                            . "Disable from tray menu or with Shift+Opt+Cmd+O."
        return
    }
    if (optspecialchars = 0) {
        Menu, Tray, Uncheck, OptSpecialChars   Shift+Opt+Cmd+O
        MsgBox, 0, ALERT, Option key special character entry scheme is now DISABLED.
        return
    }
    return

; #IfWinNotActive ahk_group remotes
#If !WinActive("ahk_group remotes") && optspecialchars = 1

    ; ######   NUMBER KEYS ROW   ######

    ; Dead_Keys_Accent_Grave
    ; ###   SC029 is ` (Grave key above Tab)
    ; Grave accent: Option+`, then key to accent
    $!SC029::
        ; Use Apple "dead keys" Option key method to attach accents to next character typed
        ; Grave accent activated by Option+` (Alt plus scan code SC029, or !SC029)
        StringCaseSense, On
        ; watch next input string
        Input, UserInput, L1 
        ; Watch for Escape key, cancel dead keys sequence
        if UserInput = Esc
            Return
        ; Option/Alt key needed to access menus sometimes
        ; If user repeats same shortcut, just send to app unmodified.
        ; else if UserInput = !SC029
        ;     Send, {Alt down}{SC029}{Alt up}
        else if UserInput = a
            ; à {U+00E0} (Alt+0224)
            Send, {U+00E0}
        else if UserInput = e
            ; è {U+00E8} (Alt+0232)
            Send, {U+00E8}
        else if UserInput = i
            ; ì {U+00EC} (Alt+0236)
            Send, {U+00EC}
        else if UserInput = o
            ; ò {U+00F2} (Alt+0242)
            Send, {U+00F2}
        else if UserInput = u
            ; ù {U+00F9} (Alt+0249)
            Send, {U+00F9}
        else if UserInput = A
            ; À {U+00C0} (Alt+0192)
            Send, {U+00C0}
        else if UserInput = E
            ; È {U+00C8} (Alt+0200)
            Send, {U+00C8}
        else if UserInput = I
            ; Ì {U+00CC} (Alt+0204)
            Send, {U+00CC}
        else if UserInput = O
            ; Ò {U+00D2} (Alt+0210)
            Send, {U+00D2}
        else if UserInput = U
            ; Ù {U+00D9} (Alt+0217)
            Send, {U+00D9}
        ; No relevant character to accent? Send input unmodified. 
        else
            Send, %UserInput%
        Return

    ; ###   SC029 is ` (Grave key above Tab)
    ; Grave Accent diacritic (non-combining) {U+0060}: ` (Alt+96)
    $!+SC029::Send, {U+0060}

    ; Inverted Exclamation Mark {U+00A1}: ¡ (Alt+0161)
    !1::Send, {U+00A1}
    ; Fraction Slash, solidus (U+2044): ⁄ (Alt+8260) [Needs Unicode]
    !+1::Send, {U+2044}

    ; Trade Mark Sign Emoji {U+2122}: ™ (Alt+0153)
    !2::Send, {U+2122}
    ; Euro currency symbol {U+20AC}: € (Alt+0128)
    !+2::Send, {U+20AC}

    ; British Pound currency symbol {U+00A3}: £ (Alt+0163)
    !3::Send, {U+00A3}
    ; Single Left-Pointing Angle Quotation mark {U+2039}: (Alt+0139)
    !+3::Send, {U+2039}

    ; Cent currency symbol {U+00A2}: ¢ (Alt+0162)
    !4::Send, {U+00A2}
    ; Single Right-Pointing Angle Quotation mark (U+203A): (Alt+0155)
    !+4::Send, {U+203A}

    ; Infinity mathematical symbol {U+221E}: ∞ (Alt+236)
    !5::Send, {U+221E}
    ; fi latin small ligature: ﬁ (U+FB01) (Alt+64257) [Needs Unicode]
    !+5::Send, {U+FB01}

    ; Section symbol {U+00A7}: § (Alt+0167)
    !6::Send, {U+00A7}
    ; fl small ligature: (U+FB02) (Alt+64258) [Needs Unicode.]
    !+6::Send, {U+FB02}

    ; Paragraph mark (Pilcrow) symbol {U+00B6}: ¶ (Alt+0182)
    !7::Send, {U+00B6}
    ; Double dagger (cross) symbol {U+2021}: ‡ (Alt+0135) [Simple dagger/cross: Alt+0134]
    !+7::Send, {U+2021}

    ; Bullet point symbol {U+2022}: • (Alt+0149) 
    !8::Send, {U+2022}
    ; Degree symbol {U+00B0}: ° (Alt+0176)
    ; NOT degree symbol: Option+0: Masculine Ordinal Indicator {U+00BA} (Alt+167 or 0186)
    ; Also NOT degree symbol: Option+k: Ring Above diacritic {U+02DA}
    !+8::Send, {U+00B0}

    ; Feminine Ordinal Indicator symbol {U+00AA}: ª (Alt+0170)
    !9::Send, {U+00AA}
    ; Middle Dot (interpunct/middot) symbol {U+00B7}: · (Alt+0183) 
    !+9::Send, {U+00B7}

    ; Masculine Ordinal Indicator symbol {U+00BA}: º (Alt+0186)
    !0::Send, {U+00BA}
    ; Single low-9 quotation mark {U+201A}: ‚ (Alt+0130) 
    !+0::Send, {U+201A}

    ; En Dash symbol {U+2013}: – (Alt+0150)
    !-::Send, {U+2013}
    ; Em Dash symbol {U+2014}: — (Alt+0151)
    !+-::Send, {U+2014}

    ; Not Equal To symbol (U+2260): ≠ (Alt+8800) [Needs Unicode]
    !=::Send, {U+2260}
    ; Plus Minus symbol {U+00B1}: ± (Alt+0177)
    !+=::Send, {U+00B1}


    ; ######   LETTER AND PUNCTUATION KEYS   ###### [ in QWERTY order ]


    ; ##############
    ; ###   1st row: Tab-key row [ qwertyuiop[]\ ] [ QWERTYUIOP{}| ]

    ; Small oe (oethel) ligature {U+0153}: œ (Alt+0156)
    !q::Send, {U+0153}
    ; Capital OE (Oethel) ligature {U+0152}: Œ (Alt+0140)
    !+q::Send, {U+0152}

    ; N-Ary Summation (sigma) notation (U+2211}: ∑ [Needs Unicode]
    $!w::Send, {U+2211}
    ; Double Low-9 Quotation mark {U+201E}: „ (Alt+0132)
    $!+w::Send, {U+201E}

    ; Dead_Keys_Accent_Acute
    ; Acute accent: Option+e, then key to accent
    $!e::
        ; Use Apple "dead keys" Option key method to attach accents to next character typed
        ; Acute accent activated by Option+e (logical Alt+e)
        StringCaseSense, On
        ; watch next input string
        Input, UserInput, L1 
        ; Watch for Escape key, cancel dead keys sequence
        if UserInput = Esc
            Return
        ; Option/Alt key needed to access menus sometimes
        ; If user repeats same shortcut, just send to app unmodified.
        ; else if UserInput = !e
        ;     Send, {Alt down}e{Alt up}
        else if UserInput = a
            ; á {U+00E1} (Alt+0225)
            Send, {U+00E1}
        else if UserInput = e
            ; é {U+00E9} (Alt+0233)
            Send, {U+00E9}
        else if UserInput = i
            ; í {U+00ED} (Alt+0237)
            Send, {U+00ED}
        else if UserInput = o
            ; ó {U+00F3} (Alt+0243)
            Send, {U+00F3}
        else if UserInput = u
            ; ú {U+00FA} (Alt+0250)
            Send, {U+00FA}
        else if UserInput = A
            ; Á {U+00C1} (Alt+0193)
            Send, {U+00C1}
        else if UserInput = E
            ; É {U+00C9} (Alt+0201)
            Send, {U+00C9}
        else if UserInput = I
            ; Í {U+00CD} (Alt+0205)
            Send, {U+00CD}
        else if UserInput = O
            ; Ó {U+00D3} (Alt+0211)
            Send, {U+00D3}
        else if UserInput = U
            ; Ú {U+00DA} (Alt+0218)
            Send, {U+00DA}
        ; No relevant character to accent? Send input unmodified. 
        else
            Send, %UserInput%
        Return

    ; Acute accent diacritic (non-combining) {U+00B4}: ´ (Alt+0180)
    !+e::Send, {U+00B4}

    ; Registered Trade Mark Sign {U+00AE}: ® (Alt+0174)
    $!r::Send, {U+00AE}
    ; Per mille symbol {U+2030}: ‰ (Alt+0137)
    $!+r::Send, {U+2030}

    ; Simple dagger (cross) symbol {U+2020}: † (Alt+0134)
    !t::Send, {U+2020}
    ; Caron/hacek diacritic (non-combining) (U+02C7): ˇ (Alt+0134)
    !+t::Send, {U+02C7}

    ; Yen currency symbol {U+00A5}: ¥ (Alt+0165)
    !y::Send, {U+00A5}
    ; Latin Capital Letter a with Acute (U+00C1): Á (Alt+0193)
    !+y::Send, {U+00C1}

    ; Dead_Keys_Accent_Umlaut
    ; Umlaut/Diaeresis accent: Option+u, then key to accent
    $!u::
        ; Use Apple "dead keys" Option key method to attach accents to next character typed
        ; Umlaut/Diaeresis accent activated by Option+u (logical Alt+u)
        StringCaseSense, On
        ; watch next input string
        Input, UserInput, L1 
        ; Watch for Escape key, cancel dead keys sequence
        if UserInput = Esc
            Return
        ; Option/Alt key needed to access menus sometimes
        ; If user repeats same shortcut, just send to app unmodified.
        ; else if UserInput = !u
        ;     Send, {Alt down}u{Alt up}
        else if UserInput = a
            ; ä {U+00E4} (Alt+0228)
            Send, {U+00E4}
        else if UserInput = e
            ; ë {U+00EB} (Alt+0235)
            Send, {U+00EB}
        else if UserInput = i
            ; ï {U+00EF} (Alt+0239)
            Send, {U+00EF}
        else if UserInput = o
            ; ö {U+00F6} (Alt+0246)
            Send, {U+00F6}
        else if UserInput = u
            ; ü {U+00FC} (Alt+0252)
            Send, {U+00FC}
        else if UserInput = y
            ; ÿ {U+00FF} (Alt+0255)
            Send, {U+00FF}
        else if UserInput = A
            ; Ä {U+00C4} (Alt+0196)
            Send, {U+00C4}
        else if UserInput = E
            ; Ë {U+00CB} (Alt+0203)
            Send, {U+00CB}
        else if UserInput = I
            ; Ï {U+00CF} (Alt+0207)
            Send, {U+00CF}
        else if UserInput = O
            ; Ö {U+00D6} (Alt+0214)
            Send, {U+00D6}
        else if UserInput = U
            ; Ü {U+00DC} (Alt+0220)
            Send, {U+00DC}
        else if UserInput = Y
            ; Ÿ {U+0178} (Alt+0159)
            Send, {U+0178}
        ; No relevant character to accent? Send input unmodified. 
        else
            Send, %UserInput%
        Return

    ; Umlaut/Diaeresis diacritic (non-combining) {U+00A8}: (Alt+0168)
    !+u::Send, {U+00A8}

    ; Dead_Keys_Accent_Circumflex
    ; Circumflex accent: Option+i, then key to accent
    $!i::
        ; Use Apple "dead keys" Option key method to attach accents to next character typed
        ; Circumflex accent activated by Option+i (logical Alt+i)
        StringCaseSense, On
        ; watch next input string
        Input, UserInput, L1 
        ; Watch for Escape key, cancel dead keys sequence
        if UserInput = Esc
            Return
        ; Option/Alt key needed to access menus sometimes
        ; If user repeats same shortcut, just send to app unmodified.
        ; else if UserInput = !i
        ;     Send, {Alt down}i{Alt up}
        else if UserInput = a
            ; â {U+00E2} (Alt+0226)
            Send, {U+00E2}
        else if UserInput = e
            ; ê {U+00EA} (Alt+0234)
            Send, {U+00EA}
        else if UserInput = i
            ; î {U+00EE} (Alt+0238)
            Send, {U+00EE}
        else if UserInput = o
            ; ô {U+00F4} (Alt+0244)
            Send, {U+00F4}
        else if UserInput = u
            ; û {U+00FB} (Alt+0251)
            Send, {U+00FB}
        else if UserInput = A
            ; Â {U+00C2} (Alt+0194)
            Send, {U+00C2}
        else if UserInput = E
            ; Ê {U+00CA} (Alt+0202)
            Send, {U+00CA}
        else if UserInput = I
            ; Î {U+00CE} (Alt+0206)
            Send, {U+00CE}
        else if UserInput = O
            ; Ô {U+00D4} (Alt+0212)
            Send, {U+00D4}
        else if UserInput = U
            ; Û {U+00DB} (Alt+0219)
            Send, {U+00DB}
        ; No relevant character to accent? Send input unmodified. 
        else
            Send, %UserInput%
        Return

    ; Modifier Letter Circumflex Accent (U+02C6): ˆ (Alt+0137)
    !+i::Send, {U+02C6}

    ; Latin Small Letter o with Stroke {U+00F8}: ø (Alt+0248)
    !o::Send, {U+00F8}
    ; Latin Capital Letter O with Stroke {U+00D8}: Ø (Alt+0216)
    !+o::Send, {U+00D8}

    ; Greek Small Letter Pi {U+03C0}: π (Alt+227)
    $!p::Send, {U+03C0}
    ; N-Ary Product mathematical symbol (U+220F): ∏ (No Alt Code) [Needs Unicode]
    $!+p::Send, {U+220F}

    ; Left Double Quotation Mark {U+201C}: “ (Alt+0147)
    $![::Send, {U+201C}
    ; Right Double Quotation Mark {U+201D}: ” (Alt+8)
    $!+[::Send, {U+201D}

    ; Left Single Quotation Mark {U+2018}: ‘ (Alt+0145)
    $!]::Send, {U+2018}
    ; Right Single Quotation Mark {U+2019}: ’ (Alt+0146)
    $+!]::Send, {U+2019}

    ; LEFT-POINTING DOUBLE ANGLE QUOTATION MARK {U+00AB}: « (Alt+0171)
    $!\::Send, {U+00AB}
    ; RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK {U+00BB}: » (Alt+0187)
    $!+\::Send, {U+00BB}


    ; ##############
    ; ###   2nd row: Caps Lock row [ asdfghjkl;' ] [ ASDFGHJKL:" ]


    ; Overring accented "a/A" used by Nordic, Greenlandic, Germanic languages
    ; 
    ; Small Letter a with Ring Above {U+00E5}: å (Alt+0229)
    $!a::Send, {U+00E5}
    ; Capital Letter A with Ring Above {U+00C5}: Å (Alt+0197)
    $!+a::Send, {U+00C5}

    ; German Eszett/beta (Sharfes/Sharp S) {U+00DF}: ß (Alt+0223)
    $!s::Send, {U+00DF}
    ; Latin Capital Letter I with Acute {U+00CD}: Í (Alt+0205)
    $!+s::Send, {U+00CD}

    ; Partial Differential mathematical symbol {U+2202}: ∂ (Alt+2202) [Needs Unicode]
    $!d::Send, {U+2202}
    ; Latin Capital Letter I with Circumflex {U+00CE}: Î (Alt+0206)
    $!+d::Send, {U+00CE}

    ; Function/florin currency symbol {U+0192}: ƒ (Alt+159)
    $!f::Send, {U+0192}
    ; Latin Capital Letter I with Diaeresis {U+00CF}: Ï (Alt+0207)
    $!+f::Send, {U+00CF}

    ; #######################################################################
    ; ##  Problem: Option+g (Win+g) brings up Windows XBox Game Bar! 
    ; ##  To remove/disable paste this text in Powershell (without quotes): 
    ; ##  "Get-AppxPackage Microsoft.XboxGamingOverlay | Remove-AppxPackage"
    ; #######################################################################
    ; Copyright Sign {U+00A9}: © (Alt+0169)
    !g::Send, {U+00A9}
    ; Double Acute Accent diacritic (non-combining) {U+02DD}: ˝ [Needs Unicode]
    !+g::Send, {U+02DD}

    ; Dot Above diacritic (non-combining) {U+02D9}: ˙ [Needs Unicode]
    $!h::Send, {U+02D9}
    ; Latin Capital Letter O with Acute {U+00D3}: Ó (Alt+0211)
    $!+h::Send, {U+00D3}

    ; Increment, laplace operator symbol {U+2206}: ∆ [Needs Unicode]
    $!j::Send, {U+2206}
    ; Latin Capital Letter O with Circumflex {U+00D4}: Ô (Alt+0212)
    $!+j::Send, {U+00D4}

    ; Ring Above diacritic (non-combining) {U+02DA}: ˚ [Needs Unicode] (NOT degree sign/symbol)
    $!k::Send, {U+02DA}
    ; Apple logo {U+F8FF}:  [Unicode Private Use Area, req's Baskerville Old Face font]
    ; $!+k::Send, {U+F8FF}    ; This Unicode address only works with Mac fonts
    $!+k::
        Send, {U+F000}    ; Change font of inserted character (may be invisible) to Baskerville Old Face
        apple_logo_alert:=1     ; Set to zero to disable, one to enable (default is enabled)
        if (apple_logo_alert=1) {
            MsgBox, 0, ALERT, % "ALERT: Change the font of the inserted character!`n`n"
                                . "Apple logo character requires the Baskerville Old Face font.`n`n`n"
                                . "Note 1: The character has been inserted but may be INVISIBLE`n"
                                . "             (i.e., non-printing) in its current font.`n`n`n"
                                . "Note 2: The inserted character will probably NOT be portable`n"
                                . "             to a Mac document/font. Use only for print/PDF `n"
                                . "             purposes on PC.`n`n`n"
                                . "Note 3: Search for apple_logo_alert in kinto.ahk config and `n"
                                . "             set it to zero to disable this MsgBox.`n`n`n"
        }
        return

    ; #######################################################################
    ; ##  Option+L works, but will also trigger the Win+L screen locking.
    ; ##  The screen locking shortcut can only be disabled in the registry. 
    ; #######################################################################
    ; Not Sign angled dash symbol {U+00AC}: ¬ (Alt+170) [Triggers Win+L screen locking!]
    $!l::Send, {U+00AC}
    ; Latin Capital Letter O with Grave {U+00D2}: Ò (Alt+0210)
    $!+l::Send, {U+00D2}

    ; Horizontal elipsis {U+2026}: … (Alt+0133)
    $!;::Send, {U+2026}
    ; Latin Capital Letter U with Acute {U+00DA}: Ú (Alt+0218)
    $!+;::Send, {U+00DA}

    ; #######################################################################
    ; ##  SC028 is single-quote key scan code
    ; #######################################################################
    ; Small ae ligature {U+00E6}: æ (Alt+0230)
    !SC028::Send, {U+00E6}
    ; Capital AE ligature {U+00C6}: Æ (Alt+0198)
    !+SC028::Send, {U+00C6}


    ; ##############
    ; ###   3rd row: Shift-Keys row [ zxcvbnm,./ ] [ ZXCVBNM<>? ]


    ; Greek Capital Letter Omega symbol {U+03A9} Ω (Alt+234)
    $!z::Send, {U+03A9}
    ; Spacing Cedilla diacritic symbol (non-combining) {U+00B8}: ¸ (Alt+0184)
    $!+z::Send, {U+00B8}

    ; Almost Equal To symbol (U+2248): ≈ (Alt+247)
    $!x::Send, {U+2248}
    ; Ogonek diacritic (non-combining) (U+02DB): ˛ (No Alt Code)
    $!+x::Send, {U+02DB}

    ; Small Letter c with Cedilla {U+00E7}: ç (Alt+0231)
    $!c::Send, {U+00E7}
    ; Capital Letter C with Cedilla {U+00C7}: Ç (Alt+0199)
    $!+c::Send, {U+00C7}

    ; Square Root radical sign (U+221A): √ (Alt+251)
    !v::Send, {U+221A}
    ; Lozenge (diamond) shape symbol (U+25CA): ◊ (No Alt Code) [Needs Unicode]
    !+v::Send, {U+25CA}

    ; Integral mathematical symbol (U+222B): ∫ (No Alt Code) [Needs Unicode]
    $!b::Send, {U+222B}
    ; Latin Small Letter Dotless i (U+0131): ı (No Alt Code) [Needs Unicode]
    $!+b::Send, {U+0131}

    ; Dead_Keys_Accent_Tilde
    ; Tilde accent: Option+n, then key to accent
    $!n::
        ; Use Apple "dead keys" Option key method to attach accents to next character typed
        ; Tilde accent activated by Option+n (logical Alt+n)
        StringCaseSense, On
        ; watch next input string
        Input, UserInput, L1 
        ; Watch for Escape key, cancel dead keys sequence
        if UserInput = Esc
            Return
        ; Option/Alt key needed to access menus sometimes
        ; If user repeats same shortcut, just send to app unmodified.
        else if UserInput = !n
            Send, {Alt down}n{Alt up}
        else if UserInput = a
            ; ã {U+00E3} (Alt+0227)
            Send, {U+00E3}
        else if UserInput = n
            ; ñ {U+00F1} (Alt+0241)
            Send, {U+00F1}
        else if UserInput = o
            ; õ {U+00F5} (Alt+0245)
            Send, {U+00F5}
        else if UserInput = A
            ; Ã {U+00C3} (Alt+0195)
            Send, {U+00C3}
        else if UserInput = N
            ; Ñ {U+00D1} (Alt+0209)
            Send, {U+00D1}
        else if UserInput = O
            ; Õ {U+00D5} (Alt+0213)
            Send, {U+00D5}
        ; No relevant character to accent? Send input unmodified. 
        else
            Send, %UserInput%
        Return

    ; Small Tilde character (U+02DC): ˜ (Alt+0152)
    !+n::Send, {U+02DC}

    ; Micro (mu) symbol {U+00B5}: µ (Alt+0181)
    $!m::Send, {U+00B5}
    ; Latin Capital Letter a with Circumflex (U+00C2): Â (Alt+0194)
    $!+m::Send, {U+00C2}

    ; Less than or equal to symbol {U+2264}: ≤ (Alt+243)
    $!,::Send, {U+2264}
    ; Macron/overline/apl overbar (non-combining) (U+00AF): ¯ (Alt+0175)
    $!+,::Send, {U+00AF}

    ; Greater than or equal to symbol {U+2265}: ≥ (Alt+242)
    $!.::Send, {U+2265}
    ; Breve diacritic (non-combining) {U+02D8}: ˘ (No Alt Code) [Needs Unicode]
    $!+.::Send, {U+02D8}

    ; Obelus/Division symbol {U+00F7}: ÷ (Alt+0247)
    $!/::Send, {U+00F7}
    ; Inverted Question Mark {U+00BF}: ¿ (Alt+0191)
    $!+/::Send, {U+00BF}

#If ; ### END of special character insertion with Option(Alt) key
