#SingleInstance, force
#NoTrayIcon
OnMessage(0x219, "notify_change") 
Return

lastkb = ""

DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

notify_change(wParam, lParam, msg, hwnd) 
{
	global lastkb
	DetectHiddenWindows On
	Run %ComSpec%,, Hide, pid
	WinWait ahk_pid %pid%
	DllCall("AttachConsole", "UInt", pid)
	WshShell := ComObjCreate("Wscript.Shell")
	exec := WshShell.Exec("cscript /nologo ""%userprofile%\.kinto\usb.vbs""")
	kbtype := exec.StdOut.ReadAll()
	DllCall("FreeConsole")
	Process Close, %pid%
	if lastkb != %kbtype%
	{

		if InStr(kbtype, "Apple")
		{
			; MsgBox, Apple
			Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" mac, "%A_ScriptDir%"
		}
		else{
			; MsgBox, Windows
			Run, "%A_ScriptDir%\NoShell.vbs" "%A_ScriptDir%\toggle_kb.bat" win, "%A_ScriptDir%"
		}
		; MsgBox % kbtype
	}
	lastkb = %kbtype%
}
