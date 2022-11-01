Dim WshShell
Set WshShell = WScript.CreateObject("WScript.Shell")
do
BtnCode = WshShell.Popup("We set up your application. Please wait... This popup will close when the application has finished setting up",0,"Setting up your app", 48)
loop