@echo off
cd /d "%~dp0"
start "Lifetime memory map server" /min python -m http.server 8765 --bind 127.0.0.1
start "" http://127.0.0.1:8765/
