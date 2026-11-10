@echo off
rem Felolvaso inditasa: szolgaltatas a 127.0.0.1:8765 cimen, majd bongeszo.
rem Mas porton:  start.bat 8767
setlocal
cd /d "%~dp0"
set PORT=%1
if "%PORT%"=="" set PORT=8765
start "" /b cmd /c "timeout /t 4 /nobreak >nul & start http://127.0.0.1:%PORT%"
uv run felolvaso --port %PORT%
endlocal
