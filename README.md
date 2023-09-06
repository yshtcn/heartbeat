# heartbeat
用python写的简易心跳工具，配合Uptime-kuma的被动监控功能（当然你也可以自己实现服务端），实现监测PC客户端的运行情况。

## 运行效果
通过访问连接，服务端会实现被动检测。同时本地访问结果会回显记录在heartbeat.log，如果服务端异常可以通过返回的代码进行故障排查。

## 使用方法

### 下载程序：
1. 下载[最新的版本](https://github.com/yshtcn/heartbeat/releases)。
2. 解压缩到任意目录

### 编辑配置文件：
运行前，记得打开把[config.Exsample.ini配置文件](https://github.com/yshtcn/heartbeat/blob/main/config.Exsample.ini)复制一份改名为config.ini，并打开配置接收心跳包的服务器地址。
如果不存在config.ini直接运行程序，程序会将config.Exsample.ini范例配置自动复制一份。

### 日志文件
心跳日志会存放在：heartbeat.log，包括时间和返回值。例如下面是一个返回200（正常值）的日志：
```
2023-08-04 11:46:15.306916 Ping: 8ms. Final URL: http://example.com/heartbeat?ping=8. Response status code: 200
```

## 执行python源代码
如果你需要直接使用源代码，可能需要用到以下几个步骤：

### 确保安装Python和必要的python库
可以从[这里下载最新的python环境](https://python.org/downloads/release/)。

使用命令行执行以下命令：
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pystray pillow requests configparser PySocks
```

如果希望自动检测python安装及必要的库支持，可以把以下内容保存为bat文件执行。
```
@echo off
cd /d %~dp0
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
@echo All Done
pause
```

### 执行批处理
每次使用py命令并不方便，可以把以下内容保存为bat文件。
```
@echo off
@echo heartbeat start
cd /d %~dp0
py heartbeat.py
pause
```

如果希望后台静默运行，可以把以下内容保存为bat文件执行。
```
@echo off
cd /d %~dp0
start pythonw heartbeat.py
```

### 打包成exe
1. 根据你的需要修改heartbeat_pyinstaller.bat,特别是如果你不希望自动更新你的pyinstaller

2. 执行heartbeat_pyinstaller.bat。


## 授权信息
项目地址： https://github.com/yshtcn/heartbeat
项目授权方式：[Apache-2.0 license](https://github.com/yshtcn/heartbeat/blob/main/LICENSE)
