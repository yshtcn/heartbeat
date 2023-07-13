import configparser
import pystray
from PIL import Image, ImageDraw
import requests
import time
import threading
import logging
from datetime import datetime
import os

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.realpath(__file__))

# 创建日志文件
log_file_path = os.path.join(current_dir, 'heartbeat.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

def create_image():
    # Generate an image and draw a pattern
    width, height = 64, 64
    color1 = "black"
    color0 = "white"
    image = Image.new('RGB', (width, height), color1)
    d = ImageDraw.Draw(image)
    d.rectangle(
        [(width // 2, 0), (width, height)],
        fill=color0)
    return image

# Create an Event object to signal the heartbeat thread to stop
stop_heartbeat = threading.Event()

def heartbeat(interval, heartbeat_url):
    while not stop_heartbeat.is_set():
        try:
            response = requests.get(heartbeat_url)
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
icon = pystray.Icon("系统心跳", image, "系统状态报送", menu=pystray.Menu(pystray.MenuItem('关闭主机状态报送', quit_action)))



# 从配置文件读取设置
config = configparser.ConfigParser()
config.read(os.path.join(current_dir, 'config.ini'))
interval = config.getint('Settings', 'interval')
heartbeat_url = config.get('Settings', 'heartbeat_url')

# Start the heartbeat function in a new thread
t = threading.Thread(target=heartbeat, args=(interval, heartbeat_url))
t.start()

icon.run(setup)
