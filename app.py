from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psutil
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

def get_drives_info():
    drives = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        # Exclude /dev/loop devices
        if 'loop' not in partition.device:
            usage = psutil.disk_usage(partition.mountpoint)
            drives.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
    return drives

def emit_system_stats():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        drives_info = get_drives_info()

        socketio.emit('system_stats', {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_info.percent,
            'drives': drives_info
        })
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    thread = threading.Thread(target=emit_system_stats)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
