@echo off
start /d . "http server" /min py http_server.py
echo http_server.py has been started minimized
timeout /t 5