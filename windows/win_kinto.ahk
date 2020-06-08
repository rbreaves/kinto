SetTitleMatchMode, 2

GroupAdd, terminals, ahk_exe ubuntu.exe
GroupAdd, terminals, ahk_exe ConEmu.exe
GroupAdd, terminals, ahk_exe ConEmu64.exe
GroupAdd, terminals, ahk_exe powershell.exe
GroupAdd, terminals, ahk_exe WindowsTerminal.exe
GroupAdd, terminals, ahk_exe Hyper.exe
GroupAdd, terminals, ahk_exe Cmd.exe
GroupAdd, terminals, Fluent Terminal ahk_class ApplicationFrameWindow

GroupAdd, posix, ahk_exe ubuntu.exe
GroupAdd, posix, ahk_exe ConEmu.exe
GroupAdd, posix, ahk_exe ConEmu64.exe
GroupAdd, posix, ahk_exe Hyper.exe
GroupAdd, posix, ahk_exe mintty.exe
GroupAdd, posix, Fluent Terminal ahk_class ApplicationFrameWindow

GroupAdd, ConEmu, ahk_exe ConEmu.exe
GroupAdd, ConEmu, ahk_exe ConEmu64.exe
GroupAdd, ConEmu, ahk_exe WindowsTerminal.exe

GroupAdd, editors, ahk_exe sublime_text.exe
GroupAdd, editors, ahk_exe VSCodium.exe
GroupAdd, editors, ahk_exe Code.exe

GroupAdd, vscode, ahk_exe VSCodium.exe
GroupAdd, vscode, ahk_exe Code.exe

; New AltTab and CtrlTab fix
*tab:: 
{
	; if (GetKeyState("Tertiary", "P") AND GetKeyState("LShift", "P") = false) {  
    if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P") = false) {
    	; Send {LCtrl down}{Secondary up}{tab}
        Send {LCtrl down}{LWin up}{tab}
        KeyWait, tab
    ; } else if (GetKeyState("Tertiary", "P") AND GetKeyState("LShift", "P")) {
    } else if (GetKeyState("LCtrl", "P") AND GetKeyState("LShift", "P")) {
    	; Send {LCtrl down}{Secondary up}{LShift down}{tab}
        Send {LCtrl down}{LWin up}{LShift down}{tab}
        KeyWait, tab
        ; return
    ; } else if (GetKeyState("Primary", "P") AND GetKeyState("LShift", "P") = false) { 
    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P") = false) {     
        Send {LAlt down}{tab}
        KeyWait, tab
    ; ; } else if (GetKeyState("Primary", "P") AND GetKeyState("LShift", "P")) { 
    } else if (GetKeyState("LAlt", "P") AND GetKeyState("LShift", "P")) {  
        Send {LAlt down}{LShift down}{tab}
        KeyWait, tab
    ; } else if (GetKeyState("Secondary", "P") AND GetKeyState("LShift", "P")) { 
    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) = false {  
        return
    ; } else if (GetKeyState("Secondary", "P") AND GetKeyState("LShift", "P")) {
    } else if (GetKeyState("LWin", "P") AND GetKeyState("LShift", "P")) {  
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

$LAlt::LCtrl
$LWin::LAlt
$LCtrl::LWin

; Hack to disable start menu on winkey
; $LCtrl up::Send {Ctrl down}{LWin up}{Ctrl up}
$LCtrl up::Send {Ctrl down}{LWin up}{Ctrl up}

; temporary hack to ensure keys don't get stuck
; impacts Alt-Tab fix
; Primary up::Send {LAlt up}{LCtrl up}
$LAlt up::Send {LWin up}{LAlt up}{LCtrl up}
; $LWin up::Send {LWin down}{LAlt up}{LCtrl up}{LWin up}

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
	; Sigint Interrupt
	; $#c::Send {Ctrl down}c{Ctrl up}

	; $#c up::Send {c up}{Ctrl up}

	; #c up::
	; SetKeyDelay -1
	; Send {c Up}{Ctrl up}
	; return

	; Copy
	^c::
	SetKeyDelay -1
	Send {Ctrl down}{Shift down}{c DownTemp}
	; return

	^c up::
	SetKeyDelay -1
	Send {c Up}{Ctrl up}{Shift up}
	; return

	; Paste
	*v::
	if (GetKeyState("LCtrl")){
		If not WinActive("ahk_group ConEmu") && not WinActive("ahk_exe cmd.exe"){
			SetKeyDelay -1
			Send {Blind}{LShift down}{v DownTemp}
		}
		else{
			Send {Blind}v
		}
	}
	return

	^v up::
	SetKeyDelay -1
	Send {Blind}{v Up}{LShift Up}
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
#If

; #IfWinActive ahk_group ConEmu
;	; Paste
;	$^v::Send {Shift down}{Insert}{Shift Up}
;	#v::Send {LCtrl down}v{LCtrl Up}
; #If

; #IfWinActive ahk_exe mintty.exe
; 	; Copy
; 	$^c::Send {Control down}{Insert}{Control Up}
; 	#c::Send {LCtrl down}c{LCtrl Up}
; 	; Paste
; 	$^v::Send {Shift down}{Insert}{Shift Up}
; 	#v::Send {LCtrl down}v{LCtrl Up}
; #If

;Disable win + l key locking (This line must come before any hotkey assignments in the .ahk file)

; Admin privileges required
; Sets Workstation Lock to not occur on Win+L
; RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Microsoft\Windows\CurrentVersion\Policies\System, DisableLockWorkstation, 1

; Re-enables Workstation lock on Ctrl+Cmd+Q
; Need to Remove Quick Assist and reboot
; Remove-WindowsCapability -online -name App.Support.QuickAssist~~~~0.0.1.0
; #^q::
;  re-enable locking workstation, then lock it
;  RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Microsoft\Windows\CurrentVersion\Policies\System, DisableLockWorkstation, 0
;  DllCall("LockWorkStation")
; Reload script to relock Workstation Lock
;  Reload 
;return