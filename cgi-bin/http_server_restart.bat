@echo on
timeout /t 20
start py

start py http_server_restart.py
echo http server error caused it to fail
timeout /t 300
exit