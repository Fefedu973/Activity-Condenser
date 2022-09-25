set currentDir=%cd%

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
    %PYTHON_MSI% /quiet InstallAllUsers=1 TargetDir=c:\Python310 PrependPath=1 Include_pip=1
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
echo Fix permissions so that Lib\site-packages and Scripts are read-
echo write capable for Limited User Accounts.
echo ------------------------------------------------------------------
echo,




echo,
echo ------------------------------------------------------------------
echo Download pywin32
echo ------------------------------------------------------------------
echo,

if not exist %PYWIN_EXE% (
    echo "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%%20%PYWIN_BUILD%/%PYWIN_EXE%"
    curl -L -O "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%%20%PYWIN_BUILD%/%PYWIN_EXE%"
    copy /y %PYWIN_EXE% c:\Python310
)


rem echo,
rem echo ------------------------------------------------------------------
rem echo Install pywin32
rem echo ------------------------------------------------------------------
rem echo,

rem if exist %PYWIN_EXE% (
rem     start /wait %PYWIN_EXE%
rem ) else (
rem     echo pywin32 installer didn't seem to download correctly.
rem     exit /b 1
rem )

echo,
echo ------------------------------------------------------------------
echo Add easy_install
echo ------------------------------------------------------------------
echo,

if not exist ez_setup.py (
    curl -O https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
)

python ez_setup.py

echo,
echo ------------------------------------------------------------------
echo Add pip
echo ------------------------------------------------------------------
echo,

if not exist get-pip.py (
    curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
)

python get-pip.py

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
echo Fix Lib\site-packages permissions to include BUILTIN\Users:R
echo according to cacls output.
echo
echo Have to do this recursively all the way down.
echo ------------------------------------------------------------------
echo,

echo y| cacls c:\Python310\Lib\site-packages\*.* /T /E /G BUILTIN\Users:R

echo,
echo ------------------------------------------------------------------
echo Python %PYTHON_VERSION%, easy_install, pip, and all the 
echo Dependencies of the project are now installed!
echo ------------------------------------------------------------------
echo,

python settings.pyw
python tray.py

pause

