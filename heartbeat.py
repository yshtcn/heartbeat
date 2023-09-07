import sys
import configparser
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import requests
import time
import threading
import logging
from datetime import datetime
import os
import shutil
import subprocess
import platform
import winreg
from plyer import notification

def display_notification(title, message, app_name='YourAppName', timeout=10):
    """
    Display a Windows notification.

    Parameters:
    - title (str): The title of the notification.
    - message (str): The message content of the notification.
    - app_name (str): The name of the application. Default is 'YourAppName'.
    - timeout (int): The time (in seconds) before the notification disappears. Default is 10 seconds.
    """
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        timeout=timeout
    )





# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.realpath(__file__))
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)  # 如果是frozen的（即打包后的exe），使用这个目录

# 创建日志文件
log_file_path = os.path.join(current_dir, 'heartbeat.log')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def create_image():
    width, height = 64, 64
    color1 = "black" 
    color0 = "white"

    image = Image.new('RGB', (width, height), color1)
    d = ImageDraw.Draw(image)

    # 画图标
    d.arc((32,0, 64,32), 0, 180, fill=color0)
    d.rectangle((0, 32, 32, 64), fill=color0)

    return image

# Create an Event object to signal the heartbeat thread to stop
stop_heartbeat = threading.Event()

def ping(host):
    # ping command, use -c or -n parameter depending on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    if platform.system().lower() == 'windows':
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Try decoding with GBK encoding first
    try:
        stdout = stdout.decode('gbk')
    except UnicodeDecodeError:
        stdout = stdout.decode(sys.getdefaultencoding(), errors='ignore')

    ping_result = ""
    for line in stdout.split('\n'):
        if 'ms' in line:
            # Extract the time value right before 'ms'
            time_str = line.split('ms')[0].strip().split(' ')[-1]
            # Remove any non-digit characters
            ping_result = ''.join(filter(str.isdigit, time_str))

    if ping_result.isdigit() and int(ping_result) < 10000:
        # If ping result is 0, change it to 1
        if int(ping_result) == 0:
            ping_result = '1'
        return ping_result

    logger.info(f"{datetime.now()} Ping command output: {repr(stdout)}")
    return "ping failed"



def heartbeat(interval, heartbeat_url, session, ping_host):
    while not stop_heartbeat.is_set():
        try:
            ping_result = ""
            if '{ping}' in heartbeat_url and ping_host:
                ping_result = ping(ping_host)
                if ping_result == "ping failed":
                    final_url = heartbeat_url.format(ping="")
                else:
                    final_url = heartbeat_url.format(ping=ping_result)
            else:
                final_url = heartbeat_url
            response = session.get(final_url)
            logger.info(f"{datetime.now()} Ping: {ping_result}ms. Final URL: {final_url}. Response status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.info(f"{datetime.now()} An error occurred: {e}")
        time.sleep(interval)

def setup(icon):
    icon.visible = True

def quit_action(icon, item):
    icon.stop()
    # Signal the heartbeat thread to stop
    stop_heartbeat.set()

image = create_image()

# 检查config.ini是否存在，如果不存在，从config.Exsample.ini复制一份
config_path = os.path.join(current_dir, 'config.ini')
if not os.path.exists(config_path):
    exsample_config_path = os.path.join(current_dir, 'config.Exsample.ini')
    if getattr(sys, 'frozen', False):
        exsample_config_path = os.path.join(sys._MEIPASS, 'config.Exsample.ini')
    shutil.copyfile(exsample_config_path, config_path)

# 从配置文件读取设置
config = configparser.ConfigParser()

# 尝试用UTF-8编码读取文件，如果失败，尝试GBK编码
try:
    config.read(config_path, encoding='utf-8')
except UnicodeDecodeError:
    config.read(config_path, encoding='gbk')

interval = config.getint('Settings', 'interval')
heartbeat_url = config.get('Settings', 'heartbeat_url')
heartbeat_ping = config.get('Settings', 'heartbeat_ping', fallback=None)

# 从配置文件获取标题和提示信息
title = config.get('Settings', 'title')
tips = config.get('Settings', 'tips')





# 添加程序到Windows启动
def add_to_startup(program_name, executable_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, executable_path)
        winreg.CloseKey(key)        
        logger.info(f"Program added to startup: Program name = {program_name}, Executable path = {executable_path}")
        display_notification(f"{program_name}已添加到自启动项", f"启动路径： {executable_path}")
    except Exception as e:
        logger.error(f"An error occurred while adding the program to startup: {e}")
        display_notification(f"{program_name}未能添加到自启动项目", f"错误原因： {e}")

# 从Windows启动中移除程序
def remove_from_startup(program_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, program_name)
        winreg.CloseKey(key)
        logger.info(f"Program removed from startup: Program name = {program_name}")
        display_notification(f"{program_name}已从自启动项移除", f"{program_name}将不再自动启动")
    except Exception as e:
        logger.error(f"An error occurred while removing the program from startup: {e}")
        display_notification(f"{program_name}未能从自启动项移除", f"错误原因： {e}")

# 检查程序是否已在Windows启动中
def is_in_startup(program_name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, program_name)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False
    
# 检查是否是通过PyInstaller打包的程序
def is_packaged():
    return getattr(sys, 'frozen', False)


# 切换Windows启动状态
def toggle_startup(icon, item):
    program_name =  title
    if is_in_startup(program_name):
        remove_from_startup(program_name)
    else:
        add_to_startup(program_name, sys.executable)

# 创建状态栏图标和菜单
menu_items = [item('关闭程序', quit_action)]

# 判断是否以.exe方式运行，添加相应菜单项
if is_packaged():
    menu_items.insert(0, item('添加/取消自启动', toggle_startup, checked=lambda text: is_in_startup("heartbeat")))
else:
    menu_items.insert(0, item('Py运行不支持自启动', lambda text: None, enabled=False))

menu = pystray.Menu(*menu_items)

# 创建并运行状态栏图标
icon = pystray.Icon(title, image, tips, menu)


#icon = pystray.Icon(title, image, tips, menu=pystray.Menu(pystray.MenuItem('关闭程序', quit_action)))

# 创建一个新的Session对象，并根据需要配置代理
session = requests.Session()
if config.get('Settings', 'proxy_enabled', fallback='0') == '1':
    session.proxies = {'http': config.get('Settings', 'proxy_url'),
                       'https': config.get('Settings', 'proxy_url')}

# Start the heartbeat function in a new thread
display_notification(f'{title}已启动', f'{tips}')
t = threading.Thread(target=heartbeat, args=(interval, heartbeat_url, session, heartbeat_ping))
t.start()

icon.run(setup)
