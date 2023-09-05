@echo off
cd /d %~dp0
rd /S /Q dist
pyinstaller --onefile --noconsole --add-data "config.Exsample.ini;." heartbeat.py
del /F /Q heartbeat.spec
rd /S /Q build