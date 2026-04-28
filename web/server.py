import threading
import json
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit

from core.scanner import WebScanner
from core.utils import init_socketio
from web.templates import HTML_TEMPLATE

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra-secret-analyzer-key'
socketio = SocketIO(app, async_mode='eventlet')

init_socketio(socketio)

scanners = {}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('start_scan')
def handle_start_scan(data):
    domain = data['domain']
    sid = request.sid
    scanner = WebScanner(domain, sid)
    scanners[sid] = scanner
    threading.Thread(target=scanner.run).start()

@socketio.on('start_monitor')
def handle_start_monitor(json_data):
    sid = request.sid
    scanner = scanners.get(sid)
    if not scanner:
        emit('log', {'msg': 'Run a scan first.', 'level': 'error'})
        return
    endpoint = json_data.get('endpoint', '')
    method = json_data.get('method', 'GET')
    data = json_data.get('data', '{}')
    interval = int(json_data.get('interval', 3600))
    if scanner.start_monitoring(endpoint, method, data, interval):
        emit('log', {'msg': 'Growth monitoring started.', 'level': 'success'})
    else:
        emit('log', {'msg': 'Monitoring already active.', 'level': 'warning'})

@socketio.on('stop_monitor')
def handle_stop_monitor():
    sid = request.sid
    scanner = scanners.get(sid)
    if scanner:
        scanner.stop_monitoring()