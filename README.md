# heartbeat
用python写的简易心跳工具，配合Uptime-kuma的被动监控功能（当然你也可以自己实现服务端），实现监测PC客户端的运行情况。

## 运行效果
通过访问连接，服务端会实现被动检测。同时本地访问结果会记录在heartbeat.log，如果服务端异常可以通过返回的代码进行故障排查。

## 使用方法

### 下载程序：
1. 下载并安装[python](https://python.org/downloads/release/)环境。
2. 下载[本项目](https://github.com/yshtcn/heartbeat/archive/refs/heads/main.zip)并且释放到任意目录下。

### 安装所有涉及到的库：

#### 方法一：手动安装：
尝试运行py和pip是否正常工作，然后安装所需的库。
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pystray pillow requests configparser PySocks
```

#### 方法二:自动安装
解压Auto-installer-package.zip，得到Auto-installer-package.bat，双击运行。批处理会先检查python和pip的安装情况。如果正确安装会自动继续安装所需的库，正常安装时，输出显示如下：
```
echo Pip detected!
echo Python detected!
...(pip的安装信息)...
All Done
```
如果提示以下任意一种情况，建议重新安装（修复安装）python：
```
pip is not installed.
```
```
Python is not installed.
```

### 编辑配置文件：
运行前，记得打开把[config.Exsample.ini配置文件](https://github.com/yshtcn/heartbeat/blob/main/config.Exsample.ini)复制一份改名为config.ini，并打开配置接收心跳包的服务器地址.
如果不存在config.ini直接运行程序，程序会将config.Exsample.ini范例配置自动复制一份。

### 前台运行：
双击运行heartbeat.bat，检查是否正常工作。正常工作时会显示一个命令行窗口，任务栏托盘会有小图标，可以右键退出。
因为会持续打开一个命令行窗口，不便于日常使用，一般只用于初次检查和排错。

### 后台运行：
双击运行heartbeat_with_pythonw.bat，任务栏托盘会有小图标，可以右键退出。
可以把heartbeat_with_pythonw.bat加入开机自动启动（例如windows启动文件夹、计划任务等），便于开机自启。

### 日志文件
心跳日志会存放在：heartbeat.log，包括时间和返回值，例如下面是一个返回200（正常值）的日志：
```
INFO:root:2023-07-23 13:35:16.764205 Response status code: 200
```
