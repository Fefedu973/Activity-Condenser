Set shell = CreateObject("WScript.Shell")
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = scriptdir
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "setup.bat", "", "", "runas", 0