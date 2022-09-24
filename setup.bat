python --version 2>NUL
if errorlevel 1 goto errorNoPython
pip install tk
pip install Pillow
pip install requests
pip install sv-ttk
pip install pypresence
pip install discord.py
pip install nest-asyncio
pip install pywin32
pip install -e C:\Users\duboi\Downloads\Bot\Activity-Condenser\infi_systray_modified
pip install darkdetect
python settings.pyw
python tray.py
exit
goto:eof

:errorNoPython
PowerShell.exe -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File ""$PSScriptRoot\python-download.ps1""' -Verb RunAs}"
pause

