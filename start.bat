pushd "%CD%"
CD /D "%~dp0"
python checkupdate.py
pause