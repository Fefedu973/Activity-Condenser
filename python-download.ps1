# This is the link to download Python 3.6.7 from Python.org
# See https://www.python.org/downloads/
$pythonUrl = "https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe"

# This is the directory that the exe is downloaded to
$tempDirectory = "$PSScriptRoot\python\"

# Installation Directory
# Some packages look for Python here
$targetDir = "$PSScriptRoot\Python3107\"

# create the download directory and get the exe file
$pythonNameLoc = $tempDirectory + "python3107.exe"
New-Item -ItemType directory -Path $tempDirectory -Force | Out-Null
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
(New-Object System.Net.WebClient).DownloadFile($pythonUrl, $pythonNameLoc)

# These are the silent arguments for the install of python
# See https://docs.python.org/3/using/windows.html
$Arguments = @()
$Arguments += "/i"
$Arguments += 'InstallAllUsers="1"'
$Arguments += 'TargetDir="' + $targetDir + '"'
$Arguments += 'DefaultAllUsersTargetDir="' + $targetDir + '"'
$Arguments += 'AssociateFiles="1"'
$Arguments += 'PrependPath="1"'
$Arguments += 'Include_doc="1"'
$Arguments += 'Include_debug="1"'
$Arguments += 'Include_dev="1"'
$Arguments += 'Include_exe="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'InstallLauncherAllUsers="1"'
$Arguments += 'Include_lib="1"'
$Arguments += 'Include_pip="1"'
$Arguments += 'Include_symbols="1"'
$Arguments += 'Include_tcltk="1"'
$Arguments += 'Include_test="1"'
$Arguments += 'Include_tools="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += 'Include_launcher="1"'
$Arguments += "/passive"

#Install Python
Start-Process $pythonNameLoc -ArgumentList $Arguments -Wait

Function Get-EnvVariableNameList {
    [cmdletbinding()]
    $allEnvVars = Get-ChildItem Env:
    $allEnvNamesArray = $allEnvVars.Name
    $pathEnvNamesList = New-Object System.Collections.ArrayList
    $pathEnvNamesList.AddRange($allEnvNamesArray)
    return ,$pathEnvNamesList
}

Function Add-EnvVarIfNotPresent {
Param (
[string]$variableNameToAdd,
[string]$variableValueToAdd
   ) 
    $nameList = Get-EnvVariableNameList
    $alreadyPresentCount = ($nameList | Where{$_ -like $variableNameToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::Machine)
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::Process)
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::User)
        $message = "Enviromental variable added to machine, process and user to include $variableNameToAdd"
    }
    else
    {
        $message = 'Environmental variable already exists. Consider using a different function to modify it'
    }
    Write-Information $message
}

Function Get-EnvExtensionList {
    [cmdletbinding()]
    $pathExtArray =  ($env:PATHEXT).Split("{;}")
    $pathExtList = New-Object System.Collections.ArrayList
    $pathExtList.AddRange($pathExtArray)
    return ,$pathExtList
}

Function Add-EnvExtension {
Param (
[string]$pathExtToAdd
   ) 
    $pathList = Get-EnvExtensionList
    $alreadyPresentCount = ($pathList | Where{$_ -like $pathToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
        $pathList.Add($pathExtToAdd)
        $returnPath = $pathList -join ";"
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::Process)
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::User)
        $message = "Path extension added to machine, process and user paths to include $pathExtToAdd"
    }
    else
    {
        $message = 'Path extension already exists'
    }
    Write-Information $message
}

Function Get-EnvPathList {
    [cmdletbinding()]
    $pathArray =  ($env:PATH).Split("{;}")
    $pathList = New-Object System.Collections.ArrayList
    $pathList.AddRange($pathArray)
    return ,$pathList
}

Function Add-EnvPath {
Param (
[string]$pathToAdd
   ) 
    $pathList = Get-EnvPathList
    $alreadyPresentCount = ($pathList | Where{$_ -like $pathToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
        $pathList.Add($pathToAdd)
        $returnPath = $pathList -join ";"
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::Process)
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::User)
        $message = "Path added to machine, process and user paths to include $pathToAdd"
    }
    else
    {
        $message = 'Path already exists'
    }
    Write-Information $message
}

Add-EnvExtension '.PY'
Add-EnvExtension '.PYW'
Add-EnvPath 'C:\Python3107\'

# Install a library using Pip
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