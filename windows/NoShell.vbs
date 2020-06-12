If WScript.Arguments.Count >= 1 Then
    ReDim arr(WScript.Arguments.Count-1)
    prog = WScript.Arguments(0)
    For i = 1 To WScript.Arguments.Count-1
        Arg = WScript.Arguments(i)
        If InStr(Arg, " ") > 1 Then Arg = """" & Arg & """"
      arr(i) = Arg
    Next

    RunCmd = Join(arr)
    ' CreateObject("Wscript.Shell").Run RunCmd, 0, True
    Set oShell = CreateObject("Shell.Application")
	oShell.ShellExecute prog, RunCmd, , "runas", 0
End If