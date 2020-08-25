#SingleInstance force
#NoEnv
#Persistent

DetectHiddenWindows, On
Run, %A_ScriptDir%\detectUSB.ahk

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
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" win, "%A_ScriptDir%"
}

mackb(){
    Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" mac, "%A_ScriptDir%"
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

SetTitleMatchMode, 2

GroupAdd, terminals, ahk_exe ubuntu.exe
GroupAdd, terminals, ahk_exe ConEmu.exe
GroupAdd, terminals, ahk_exe ConEmu64.exe
GroupAdd, terminals, ahk_exe powershell.exe
GroupAdd, terminals, ahk_exe WindowsTerminal.exe
GroupAdd, terminals, ahk_exe Hyper.exe
GroupAdd, terminals, ahk_exe mintty.exe
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

GroupAdd, browsers, ahk_exe chrome.exe
GroupAdd, browsers, ahk_exe opera.exe
GroupAdd, browsers, ahk_exe firefox.exe
; Disable Key Remapping for Virtual Machines
; Disable for Remote desktop solutions too
GroupAdd, virtm, ahk_exe VirtualBoxVM.exe

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
    $^Backspace::Send +{Home}{Delete}
    !Backspace::Send ^{Backspace}
    !Left::Send ^{Left}
    !+Left::Send ^+{Left}
    !Right::Send ^{Right}
    !+Right::Send ^+{Right}

    ; Cmd+Space Alternative
    $^Space::Send ^{Esc}

    #IfWinActive ahk_group intellij
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
        #Space::Send ^{Space}           ;Basic code completion
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
        $^Backspace::Send ^y             ;Delete line at caret
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
        !Space::Send ^+i                ;Open quick definition lookup
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
    #If

    ; Sublime Text Remaps for VS Code
    #IfWinActive ahk_group vscode
        #p::send {Up}                                        ; Allow for traversing quick list
        #n::send {Down}                                      ; Allow for traversing quick list
        #Space::Send ^{Space}                                ; Basic code completion
        ; Remap Ctrl+Shift to behave like macOS Sublimetext
        ; Will extend cursor to multiple lines
    ;    #+Up::send ^!{Up}                                   ; ST2CODE
    ;    #+Down::send ^!{Down}                               ; ST2CODE
        ; Remap Ctrl+Cmd+G to select all matches
    ;    #^g::send ^+{L}                                     ; ST2CODE
        !+g::send ^+{G}                                     ; View source control
        ; Sigints - interrupt
        $#c::Send {Ctrl down}c{Ctrl up}
    #If

    #IfWinActive ahk_exe sublime_text.exe
        #Space::Send ^{Space}                                   ; Basic code completion
        #^Up::send !{O}                                         ; Switch file
        #^f::send {F11}                                         ; toggle_full_screen
        ^!v::send {Ctrl Down}k{Ctrl Up}{Ctrl Down}v{Ctrl Up}    ; paste_from_history
        ^Up::Return                                             ; cancel scroll_lines up
        ^!Up::send ^{Up}                                        ; scroll_lines up
        ^Down::Return                                           ; cancel scroll_lines down
        ^!Down::send ^{Down}                                    ; scroll_lines down
        #+Up::send {shift up}^!{Up}                             ; multi-cursor up
        #+Down::send {shift up}^!{Down}                         ; multi-cursor down
        ^PgDn::Return                                           ; cancel next_view
        ^PgUp::Return                                           ; cancel prev_view
        ^+{::send ^{PgDn}                                       ; next_view
        ^+}::send ^{PgUp}                                       ; prev_view
        ^!Right::send ^{PgDn}                                   ; next_view
        ^!Left::send ^{PgUp}                                    ; prev_view
        Insert::Return                                          ; cancel toggle_overwrite
        ^!O::send {Insert}                                      ; toggle_overwrite
        !c::Return                                              ; cancel toggle_case_sensitive
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
        #^g::send !{F3}                                         ; find_all_under
        ^+Up::Return                                            ; cancel swap_line_up
        #!Up::send ^+{Up}                                       ; swap_line_up
        ^+Down::Return                                          ; cancel swap_line_down
        #!Down::send ^+{Down}                                   ; swap_line_down
        ^Pause::Return                                          ; cancel cancel_build
        #c::send ^{Pause}                                       ; cancel_build
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
        #e::
        Send {End}
        return

        ; Beginning of Line
        #a::
        Send {Home}
        return

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
        If WinActive("ahk_exe mintty.exe"){
            Send {Shift down}{Insert}{Shift up}
        }
        else if WinActive("ahk_group posix"){
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
#If