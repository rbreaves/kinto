GroupAdd, terminals, ahk_exe ubuntu.exe

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
	^c::Send {LCtrl down}{LShift down}c{LCtrl Up}{LShift Up}
	#c::Send {LCtrl down}c{LCtrl Up}
	#x::Send {LCtrl down}x{LCtrl Up}
	#o::Send {LCtrl down}o{LCtrl Up}
	#r::Send {LCtrl down}r{LCtrl Up}
	#w::Send {LCtrl down}w{LCtrl Up}
	#\::Send {LCtrl down}\{LCtrl Up}
	#k::Send {LCtrl down}k{LCtrl Up}
	#u::Send {LCtrl down}u{LCtrl Up}
	#j::Send {LCtrl down}j{LCtrl Up}
	#t::Send {LCtrl down}t{LCtrl Up}
	#_::Send {LCtrl down}_{LCtrl Up}
	^v::Send {LCtrl down}{LShift down}v{LCtrl Up}{LShift Up}
#If

#IfWinActive ahk_exe powershell.exe
	^c::Send {LCtrl down}{LShift down}c{LCtrl Up}{LShift Up}
	#c::Send {LCtrl down}c{LCtrl Up}
#If