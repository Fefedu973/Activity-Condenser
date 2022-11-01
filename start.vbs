Set shell = CreateObject("WScript.Shell")
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = scriptdir
shell.Run "setup.bat", 0, False