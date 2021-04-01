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
GroupAdd, virtm, ahk_exe VirtualBoxVM.exe
GroupAdd, virtm, ahk_exe mstsc.exe

; Disabled Edge for now - no ability to close all instances
; GroupAdd, browsers, Microsoft Edge ahk_class ApplicationFrameWindow

GroupAdd, vscode, ahk_exe VSCodium.exe
GroupAdd, vscode, ahk_exe Code.exe

GroupAdd, vstudio, ahk_exe devenv.exe

GroupAdd, intellij, ahk_exe idea.exe
GroupAdd, intellij, ahk_exe idea64.exe

; SetCapsLockState, AlwaysOff ; CB/IBM

#IfWinNotActive ahk_group virtm

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
    $!Down::Send {PgDn};
    $!Up::Send {PgUp};

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

    #IfWinNotActive ahk_group terminals
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
        ^q::send {Alt Down}f{Alt Up}x   ; exit all windows
        ; Dev Tools
        !^i::send {Ctrl Down}{Shift Down}i{Shift Up}{Ctrl Up}
        !^j::send {Ctrl Down}{Shift Down}j{Shift Up}{Ctrl Up}
        ; Open preferences
        #IfWinActive ahk_exe firefox.exe
            ^,::send, {Ctrl Down}t{Ctrl Up}about:preferences{Enter}
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
        ; !c::Send ^{c}                                           ; CB/IBM
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
        ; $!c::send ^{c}                                          ; CB/IBM - Sigint
        ^!c::send !{c}                                          ; toggle_case_sensitive
        ; ^h::Return                                              ; cancel replace
        ^!f::send ^{h}                                          ; replace
        ^+h::Return                                             ; cancel replace_next
        ^!e::send ^+{h}                                         ; replace_next
        F3::Return                                              ; cancel find_next
        ^g::send {F3}                                           ; find_next
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
        #0::Send {LCtrl down}0{Ctrl up}  ; Default
        #1::Send {LCtrl down}1{Ctrl up}  ; Default
        #2::Send {LCtrl down}2{Ctrl up}  ; Default
        #3::Send {LCtrl down}3{Ctrl up}  ; Default
        #4::Send {LCtrl down}4{Ctrl up}  ; Default
        #5::Send {LCtrl down}5{Ctrl up}  ; Default
        #6::Send {LCtrl down}6{Ctrl up}  ; Default
        #7::Send {LCtrl down}7{Ctrl up}  ; Default
        #8::Send {LCtrl down}8{Ctrl up}  ; Default
        #9::Send {LCtrl down}9{Ctrl up}  ; Default
        #-::Send {LCtrl down}-{Ctrl up}  ; Default
        #=::Send {LCtrl down}={Ctrl up}  ; Default
        #`::Send {LCtrl down}`{Ctrl up}  ; Default
        #a::Send {LCtrl down}a{Ctrl up}  ; Default
        #b::Send {LCtrl down}b{Ctrl up}  ; Default
        #c::Send {LCtrl down}c{Ctrl up}  ; Default
        #d::Send {LCtrl down}d{Ctrl up}  ; Default
        #e::Send {LCtrl down}e{Ctrl up}  ; Default
        #f::Send {LCtrl down}f{Ctrl up}  ; Default
        #g::Send {LCtrl down}g{Ctrl up}  ; Default
        #h::Send {LCtrl down}h{Ctrl up}  ; Default
        #i::Send {LCtrl down}i{Ctrl up}  ; Default
        #j::Send {LCtrl down}j{Ctrl up}  ; Default
        #k::Send {LCtrl down}k{Ctrl up}  ; Default
        #l::Send {LCtrl down}l{Ctrl up}  ; Default
        #m::Send {LCtrl down}m{Ctrl up}  ; Default
        #n::Send {LCtrl down}n{Ctrl up}  ; Default
        #o::Send {LCtrl down}o{Ctrl up}  ; Default
        #p::Send {LCtrl down}p{Ctrl up}  ; Default
        #q::Send {LCtrl down}q{Ctrl up}  ; Default
        #r::Send {LCtrl down}r{Ctrl up}  ; Default
        #s::Send {LCtrl down}s{Ctrl up}  ; Default
        #t::Send {LCtrl down}t{Ctrl up}  ; Default
        #u::Send {LCtrl down}u{Ctrl up}  ; Default
        #v::Send {LCtrl down}v{Ctrl up}  ; Default
        #w::Send {LCtrl down}w{Ctrl up}  ; Default
        #x::Send {LCtrl down}x{Ctrl up}  ; Default
        #y::Send {LCtrl down}y{Ctrl up}  ; Default
        #z::Send {LCtrl down}z{Ctrl up}  ; Default
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