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
LWin & vk07::return
LWin::return
RWin & vk07::return
RWin::return
^Space::Send ^{Esc}
; ^Space::run AppName

; Cmd Tab For App Switching
LCtrl & Tab::AltTab
RCtrl & Tab::AltTab

; Ctrl Tab for In-App Tab Switching
; https://autohotkey.com/board/topic/72433-controltab/
#if GetKeyState("LWin")
*Tab::
if(!GetKeyState("LControl"))
	Send {LControl Down}
Send {Tab}
SetTimer, WaitForWinUp, 10
ToolTip trigger
return

WaitForWinUp:
if(!GetKeyState("LWin", "P"))
{
	Send {LControl Up}
	SetTimer, WaitForWinUp, Off
}
return

; Sublime Text Remaps for VS Code
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
	^c::Send {LCtrl down}{LShift down}c{LCtrl Up}{LShift Up}
	#c::Send {LCtrl down}c{LCtrl Up}
	; Paste
	$^v::
	If not WinActive("ahk_group ConEmu") && not WinActive("ahk_exe cmd.exe"){
	 	Send {LCtrl down}{LShift down}v{LCtrl Up}{LShift Up}
	}
	else{
		Send ^v
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
	#e::Send {LCtrl down}e{LCtrl Up}
	^e::return
	; Beginning of Line
	#a::Send {LCtrl down}a{LCtrl Up}
	^a::return
	;^l::Send clear{Enter}
	;#l::return
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

#IfWinActive ahk_exe mintty.exe
	; Copy
	$^c::Send {Control down}{Insert}{Control Up}
	#c::Send {LCtrl down}c{LCtrl Up}
	; Paste
	$^v::Send {Shift down}{Insert}{Shift Up}
	#v::Send {LCtrl down}v{LCtrl Up}
#If

;Disable win + l key locking (This line must come before any hotkey assignments in the .ahk file)

; Admin privileges required
; Sets Workstation Lock to not occur on Win+L
; RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Microsoft\Windows\CurrentVersion\Policies\System, DisableLockWorkstation, 1

; Re-enables Workstation lock on Ctrl+Cmd+Q
; Need to Remove Quick Assist and reboot
; Remove-WindowsCapability -online -name App.Support.QuickAssist~~~~0.0.1.0
#^q::
;  re-enable locking workstation, then lock it
;  RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Microsoft\Windows\CurrentVersion\Policies\System, DisableLockWorkstation, 0
;  DllCall("LockWorkStation")
; Reload script to relock Workstation Lock
;  Reload 
;return