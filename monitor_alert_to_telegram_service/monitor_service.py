import psutil
import requests
import time

# Configuration
TELEGRAM_TOKEN = '7211412404:AAFTO0ud7ljRciRCCleffFZFKqdxKESzSGs'
CHAT_ID = '5550108562'
CPU_THRESHOLD = 99
MEMORY_THRESHOLD = 33
DRIVE_THRESHOLD = 90
CHECK_INTERVAL = 1  # seconds

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending message: {e}")

def check_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    drives_info = psutil.disk_partitions()
    
    message = ""
    
    if cpu_usage > CPU_THRESHOLD:
        message += f"⚠️ High CPU Usage: {cpu_usage}%\n"
    
    if memory_info.percent > MEMORY_THRESHOLD:
        message += f"⚠️ High Memory Usage: {memory_info.percent}%\n"
    
    for partition in drives_info:
        if 'loop' not in partition.device:
            usage = psutil.disk_usage(partition.mountpoint)
            if usage.percent > DRIVE_THRESHOLD:
                message += f"⚠️ Drive {partition.device} at {usage.percent}% usage\n"
    
    if message:
        send_telegram_message(message)

if __name__ == "__main__":
    while True:
        check_system_stats()
        time.sleep(CHECK_INTERVAL)
