Option Explicit
Dim oWMISrv, collDvcs, iUSBDvc , iDvc, sDvcID, sPID, sVID, deviceID

' add item to array
Function AddItem(arr, val)
    ReDim Preserve arr(UBound(arr) + 1)
    arr(UBound(arr)) = val
    AddItem = arr
End Function

' returns an array of the unique items in for-each-able collection fex
Function uniqFE(fex)
	Dim dicTemp : Set dicTemp = CreateObject("Scripting.Dictionary")
	Dim xItem
	For Each xItem In fex
		dicTemp(xItem) = 0
	Next
	uniqFE = dicTemp.Keys()
End Function

Function ReplaceX(ByVal sValue, ByVal sPattern, ByVal sNValue)
    Dim oReg : Set oReg = New RegExp
    oReg.Pattern = sPattern
    ReplaceX = oReg.Replace(sValue, sNValue)
    Set oReg = Nothing
End Function

Set oWMISrv = GetObject("winmgmts:\\.\root\cimv2")
Set collDvcs = oWMISrv.ExecQuery("Select * From Win32_PnPEntity WHERE Service='kbdhid'")

Dim deviceVID : deviceVID=Array()
Dim devicePID : devicePID=Array()
Dim deviceDesc : deviceDesc=Array()
Dim counter: counter=0

For Each iUSBDvc In collDvcs
    sVID = ReplaceX(iUSBDvc.DeviceID, ".*VID_(.{4}).*", "$1")
    sPID = ReplaceX(iUSBDvc.DeviceID, ".*PID_(.{4}).*", "$1")
    deviceVID = AddItem(deviceVID, sVID)
    devicePID = AddItem(devicePID, sPID)
    deviceDesc = AddItem(deviceDesc, iUSBDvc.Description)
    counter = counter + 1
    ' Wscript.Echo "Name : "& iUSBDvc.Description &"VID_PID : "& sVID & sPID
    Next

Dim uniqueVID: uniqueVID = uniqFE(deviceVID)
Dim vcount: vcount = UBound(uniqueVID) + 1
Dim nonApple: nonApple = 0
Dim i

If vcount = 1 Then
	deviceID = deviceVID(0)
	If StrComp(deviceVID(0), "05AC") = 0 Then
		Wscript.Echo "Apple " & deviceID
	Else
		Wscript.Echo "Windows " & deviceID
	End If
Else
	For i = 0 To counter-1
		deviceID = deviceVID(i)
    	If StrComp(deviceVID(i), "05AC") = -1 Then
    		nonApple = 1
    	End If
	Next
	If nonApple = 1 Then
		Wscript.Echo "Windows " & deviceID
	Else
		Wscript.Echo "Apple " & deviceID
	End If
End If

Set collDvcs = Nothing
Set oWMISrv = Nothing