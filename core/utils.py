import numpy as np
import random
import requests
import time
from urllib.parse import urljoin, urlparse
from core.config import USER_AGENTS, CLASS_PATTERNS

_socketio = None

def init_socketio(sio):
    global _socketio
    _socketio = sio

def random_user_agent():
    return random.choice(USER_AGENTS)

def log_emit(sid, message, level="info"):
    if _socketio:
        _socketio.emit('log', {'msg': message, 'level': level}, room=sid)

def progress_emit(sid, percent, text=""):
    if _socketio:
        _socketio.emit('progress', {'percent': percent, 'text': text}, room=sid)

def classify_endpoint(url):
    categories = []
    lower = url.lower()
    for cat, keywords in CLASS_PATTERNS.items():
        if any(kw in lower for kw in keywords):
            categories.append(cat)
    return categories if categories else ["unknown"]

def entropy(ids):
    if not ids:
        return 0
    value, counts = np.unique(ids, return_counts=True)
    probs = counts / len(ids)
    ent = -np.sum(probs * np.log2(probs))
    max_ent = np.log2(len(ids)) if len(ids) > 1 else 1
    return ent / max_ent if max_ent != 0 else 0

def get_rendered_html(url, session, sid):
    try:
        resp = session.get(url, timeout=15)
        html = resp.text
        if len(html) < 500 and ('<div id="root"' in html or '<div id="app"' in html or '<noscript' in html):
            log_emit(sid, "SPA detected – activating headless browser...", "info")
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                options = Options()
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--ignore-certificate-errors')
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(url)
                time.sleep(5)
                rendered = driver.page_source
                driver.quit()
                if len(rendered) > len(html):
                    log_emit(sid, f"JS‑rendered HTML captured (length {len(rendered)})", "success")
                    return rendered
            except Exception as e:
                log_emit(sid, f"Selenium unavailable or error: {e}", "warning")
        return html
    except Exception as e:
        log_emit(sid, f"Error fetching page: {e}", "error")
        return ""