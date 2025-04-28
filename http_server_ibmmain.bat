@echo off
start /d %USERPROFILE%\Documents\jon\ibm-main "http server" /min py http_server.py
echo http_server.py has been started minimized
timeout /t 5