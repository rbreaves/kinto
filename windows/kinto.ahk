GroupAdd, terminals, ahk_exe ubuntu.exe
GroupAdd, terminals, ahk_exe ConEmu.exe
GroupAdd, terminals, ahk_exe ConEmu64.exe
GroupAdd, terminals, ahk_exe powershell.exe

GroupAdd, posix, ahk_exe ubuntu.exe
GroupAdd, posix, ahk_exe ConEmu.exe
GroupAdd, posix, ahk_exe ConEmu64.exe
GroupAdd, posix, ahk_exe mintty.exe

GroupAdd, ConEmu, ahk_exe ConEmu.exe
GroupAdd, ConEmu, ahk_exe ConEmu64.exe

GroupAdd, editors, ahk_exe sublime_text.exe

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
LWin & Tab::Send ^{Tab}
RWin & Tab::Send ^{Tab}

; Close Apps
^q::Send !{F4}

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

#IfWinActive ahk_group editors
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
#If

#IfWinActive ahk_group posix
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
#If

#IfWinActive ahk_group ConEmu
	; Paste
	$^v::Send {Shift down}{Insert}{Shift Up}
	#v::^v
#If

#IfWinActive ahk_exe mintty.exe
	; Copy
	$^c::Send {Control down}{Insert}{Control Up}
	#c::Send {LCtrl down}c{LCtrl Up}
	; Paste
	$^v::Send {Shift down}{Insert}{Shift Up}
	#v::Send {LCtrl down}v{LCtrl Up}
#If

#IfWinActive ahk_exe ubuntu.exe
	; Paste
	^v::Send {LCtrl down}{LShift down}v{LCtrl Up}{LShift Up}
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