import sys
import configparser
import pystray
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

icon = pystray.Icon(title, image, tips, menu=pystray.Menu(pystray.MenuItem('关闭程序', quit_action)))

# 创建一个新的Session对象，并根据需要配置代理
session = requests.Session()
if config.get('Settings', 'proxy_enabled', fallback='0') == '1':
    session.proxies = {'http': config.get('Settings', 'proxy_url'),
                       'https': config.get('Settings', 'proxy_url')}

# Start the heartbeat function in a new thread
t = threading.Thread(target=heartbeat, args=(interval, heartbeat_url, session, heartbeat_ping))
t.start()

icon.run(setup)
