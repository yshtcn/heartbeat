# heartbeat
用python写的简易心跳工具，配合Uptime-kuma的被动监控功能监测PC客户端的运行情况。

## 直接运行：
```
py heartbeat.py
```
观察是否出错，一般错误主要是因为缺少所需的库造成的。

## 安装所有涉及到的库：
这里使用了清华大学的源进行安装。
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pystray pillow requests configparser
```


## 后台运行：
```
pythonw heartbeat.py
```

可以创建一个批处理启动，这里可以使用start命令，也可以用windows计划任务自动启动。
```
start pythonw heartbeat.py
```

