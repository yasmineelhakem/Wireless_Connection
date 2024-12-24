from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import re
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('my event')
def handle_my_event(json):
    print('Received event: ' + str(json))

@socketio.on('fetch_networks')
def fetch_networks():
    p = subprocess.Popen("netsh wlan show networks mode=bssid", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()

    if platform.system() == 'Windows':
        networks = re.findall(r"^SSID\s+\d+\s+:\s+([A-Za-z0-9-_' ]+).*?Signal\s+:\s+([0-9]+)%", out, re.MULTILINE | re.DOTALL)
    elif platform.system() == 'Linux':
        networks= re.findall('(wlan [0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
    else:
        print('Unsupported Operating System')
        return

    if networks:
        max_signal = max(networks, key=lambda x: int(x[1]))
        print(networks)
        emit('update_networks', {'networks': networks, 'max_signal': max_signal})
    else:
        emit('update_networks', {'networks': [], 'max_signal': None})

@socketio.on('connect_to_network')
def connect_to_network(data):
    print('wselt lel py ',data['ssid'])
    p = subprocess.Popen(f"netsh wlan connect name={data['ssid']}", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    print(out)
    emit('connection_status',{'message' : out})

if __name__ == '__main__':
    socketio.run(app, debug=True)