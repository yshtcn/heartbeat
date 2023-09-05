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
