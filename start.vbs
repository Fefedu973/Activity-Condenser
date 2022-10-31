Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
scriptfile = scriptdir & "\start.bat"
strArgs = "cmd /c" & scriptfile
oShell.Run strArgs, 0, false