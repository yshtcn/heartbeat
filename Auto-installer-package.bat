@echo off
setlocal enabledelayedexpansion

:: 检查pip
for /f "tokens=1" %%i in ('pip --version 2^>^&1 ^| findstr /C:"pip"') do (
    set PIPVER=%%i
)
if "!PIPVER!" == "pip" (
    echo Pip detected!
) else (
    echo Error: pip is not installed.
    pause
    exit /b 1
)

:: 检查python
for /f "tokens=1" %%h in ('python --version 2^>^&1') do (
    set PYVER2=%%h
)
if "!PYVER2!" == "Python" (
    echo Python detected!
) else (
    echo Error: Python is not installed.
    pause
    exit /b 1
)
endlocal

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pystray pillow requests configparser PySocks
@echo 安装完成
pause
