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

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.realpath(__file__))

# 创建日志文件
log_file_path = os.path.join(current_dir, 'heartbeat.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

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

def heartbeat(interval, heartbeat_url, session):
    while not stop_heartbeat.is_set():
        try:
            response = session.get(heartbeat_url)
            logging.info(f"{datetime.now()} Response status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.info(f"{datetime.now()} An error occurred: {e}")
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

# 从配置文件获取标题和提示信息
title = config.get('Settings', 'title')
tips = config.get('Settings', 'tips')

icon = pystray.Icon(title, image, tips, menu=pystray.Menu(pystray.MenuItem(tips, quit_action)))

# 创建一个新的Session对象，并根据需要配置代理
session = requests.Session()
if config.get('Settings', 'proxy_enabled', fallback='0') == '1':
    session.proxies = {'http': config.get('Settings', 'proxy_url'),
                       'https': config.get('Settings', 'proxy_url')}

# Start the heartbeat function in a new thread
t = threading.Thread(target=heartbeat, args=(interval, heartbeat_url, session))
t.start()

icon.run(setup)
