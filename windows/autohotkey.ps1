if(-not(Get-Command "choco" -errorAction SilentlyContinue)){
    Write-Output "Seems Chocolatey is not installed, installing now"
    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}
else{
    Write-Output "Chocolatey is already installed"
}

if(-not(test-path "C:\Program Files\AutoHotkey\AutoHotkey.exe")){
	choco install autohotkey.install
}
if(-not(test-path "C:\Strawberry\")){
	choco install strawberryperl
}
