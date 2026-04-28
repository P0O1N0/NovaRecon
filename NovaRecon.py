#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import importlib
import pkgutil

def install_and_import(package, pip_name=None):
    if pip_name is None:
        pip_name = package
    if pkgutil.find_loader(package) is None:
        print(f"[!] Installing {pip_name} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    globals()[package] = importlib.import_module(package)

try:
    import eventlet
except ImportError:
    install_and_import("eventlet")
    import eventlet
eventlet.monkey_patch()

dependencies = {
    "flask": "flask",
    "flask_socketio": "flask-socketio",
    "requests": "requests",
    "bs4": "beautifulsoup4",
    "colorama": "colorama",
    "selenium": "selenium",
    "webdriver_manager": "webdriver-manager",
    "numpy": "numpy",
}
for mod, pip_name in dependencies.items():
    try:
        __import__(mod)
    except ImportError:
        install_and_import(mod, pip_name)
        __import__(mod)

from web.server import app, socketio
import webbrowser
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

if __name__ == '__main__':
    print(Fore.CYAN + Style.BRIGHT + """
    ██╗    ██╗███████╗██████╗      █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗███████╗██████╗ 
    ██║    ██║██╔════╝██╔══██╗    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝    ███████║██╔██╗ ██║███████║██║   ╚████╔╝   ███╔╝ █████╗  ██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝  ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████╗███████╗██║  ██║
     ╚══╝╚══╝ ╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
    """)
    print(Fore.GREEN + " NovaRecon v1.2 – Web Intelligence Scanner")
    print(Fore.YELLOW + " Opening browser... Enter a domain and start the analysis.\n")
    webbrowser.open('http://127.0.0.1:5000')
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)