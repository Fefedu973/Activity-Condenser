pushd "%CD%"
CD /D "%~dp0"


set currentDir=%cd%

Del “%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python.exe”
Del “%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\python3.exe”


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
pip install -e "%currentDir%\infi_systray_modified"
pip install darkdetect
python settings.pyw
python tray.py
pause
goto:eof

:errorNoPython
@echo off

set PYTHON_VERSION=3.10.7
set PYTHON_MSI=python-%PYTHON_VERSION%-amd64.exe  
set PYTHON_EXE=c:\Python310\python.exe
set PYTHON_PATH=c:\Python310;c:\Python310\Scripts
set PYTHON_APPDATA=c:\Python310\AppData

set PYWIN_BUILD=218
set PYWIN_EXE=pywin32-%PYWIN_BUILD%.win32-py2.7.exe

echo,
echo ------------------------------------------------------------------
echo Download Python
echo ------------------------------------------------------------------
echo,

if not exist %PYTHON_EXE% (
if not exist %PYTHON_MSI% (
    curl -L -O http://python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_MSI%
)
)

echo,
echo ------------------------------------------------------------------
echo Install Python
echo ------------------------------------------------------------------
echo,

if not exist %PYTHON_EXE% (
if exist %PYTHON_MSI% (
    %PYTHON_MSI% /quiet InstallAllUsers=1 PrependPath=1 TargetDir=c:\Python310  Include_pip=1
) else (
    echo Python installer package didn't seem to download correctly.
    exit /b 1
)
)

echo,
echo ------------------------------------------------------------------
echo Add Python to PATH
echo ------------------------------------------------------------------
echo,

rem Add the PYTHON_PATH to the PATH environment variable.

rem reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "%PYTHON_PATH%"
rem reg add "HKLM\SYSTEM\ControlSet001\Control\Session Manager\Environment" /v PATH /t REG_EXPAND_SZ /d "%PATH%;c:\Python310;c:\Python310\Scripts"
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /f /v PATH /t REG_EXPAND_SZ /d "%PATH%;%PYTHON_PATH%"

rem Set LOCALAPPDATA to APPDATA, otherwise distlib will throw errors.
rem See: https://vilimpoc.org/blog/2014/01/18/time-robbing-python-errors/

mkdir %PYTHON_APPDATA%
reg add "HKLM\System\CurrentControlSet\Control\Session Manager\Environment" /f /v LOCALAPPDATA /t REG_SZ /d "%PYTHON_APPDATA%"

rem Temporarily set LOCALAPPDATA.
set LOCALAPPDATA=%PYTHON_APPDATA%

rem Temporarily set the path, so we can use the python command.
set PATH=%PATH%;%PYTHON_PATH%

echo,
echo ------------------------------------------------------------------
echo Install Dependencies
echo ------------------------------------------------------------------
echo,

pip install tk
pip install Pillow
pip install requests
pip install sv-ttk
pip install pypresence
pip install discord.py
pip install nest-asyncio
pip install pywin32
pip install darkdetect
pip install -e "%currentDir%\infi_systray_modified"

echo,
echo ------------------------------------------------------------------
echo Python %PYTHON_VERSION%, easy_install, pip, and all the 
echo Dependencies of the project are now installed!
echo ------------------------------------------------------------------
echo,

python settings.pyw
python tray.py

pause

