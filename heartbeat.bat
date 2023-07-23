@echo off
@echo heartbeat start
cd /d %~dp0
py heartbeat.py
pause
