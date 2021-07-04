Invoke-WebRequest -Uri https://github.com/rbreaves/kinto/archive/refs/heads/master.zip -OutFile $env:USERPROFILE\Downloads\kinto.zip
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\kinto.zip" -DestinationPath "$env:USERPROFILE\Downloads" -Force
Set-ExecutionPolicy Bypass -Scope Process -Force
iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
choco install -y python3
cd "$env:USERPROFILE\Downloads\kinto-master"
py .\setup.py