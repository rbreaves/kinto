#SingleInstance, force
OnMessage(0x219, "notify_change") 
Return

lastnotify := 0

notify_change(wParam, lParam, msg, hwnd) 
{
	global lastnotify
	T = %A_Now%
	T -= 19700101000000,seconds
	Tdiff := T
	Tdiff -= lastnotify
	if Tdiff > 5 
	{
		MsgBox % Tdiff
	}
	lastnotify := T
}