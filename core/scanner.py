import socket
import ssl
import json
import re
import time
import random
import threading
import math
import numpy as np
from urllib.parse import urlparse, urljoin
from datetime import datetime
from collections import defaultdict
import requests
from bs4 import BeautifulSoup

from core.config import COMMON_DIRS, SENSITIVE_FILES, COMMON_ACTION_NAMES, CLASS_PATTERNS
from core.utils import random_user_agent, log_emit, progress_emit, classify_endpoint, entropy, get_rendered_html

class WebScanner:
    def __init__(self, domain, sid):
        self.domain = domain if domain.startswith(('http://', 'https://')) else 'http://' + domain
        self.parsed = urlparse(self.domain)
        self.base_url = f"{self.parsed.scheme}://{self.parsed.netloc}"
        self.sid = sid
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': random_user_agent()})
        self.results = {
            'domain_info': {},
            'server': {},
            'ssl': {},
            'security_headers': {},
            'vulnerabilities': [],
            'endpoints': [],
            'id_analysis': [],
            'emails': [],
            'social': [],
            'interesting_files': [],
            'directory_listing': [],
            'html_comments': [],
            'forms': [],
            'other_info': {}
        }
        self.monitoring_active = False
        self.monitor_thread = None
        self.progress_steps = 10
        self.current_step = 0
        self.scores = {
            'security': 100,
            'data_exposure': 0,
            'id_reliability': 0
        }
        self.growth_data = []

    def delay(self):
        time.sleep(random.uniform(2.0, 4.0))

    def run(self):
        try:
            self._basic_info()
            self._fetch_homepage()
            self._check_common_endpoints()
            self._vulnerability_checks()
            self._id_hunting()
            self._finalize()
        except Exception as e:
            log_emit(self.sid, f"Critical error: {str(e)}", "error")
        finally:
            from core.utils import _socketio
            if _socketio:
                _socketio.emit('scan_complete', {'results': self.results, 'scores': self.scores}, room=self.sid)

    def _step(self, text=""):
        self.current_step += 1
        pct = int((self.current_step / self.progress_steps) * 100)
        progress_emit(self.sid, pct, text)

    def _basic_info(self):
        self._step("Gathering basic domain info...")
        log_emit(self.sid, "Resolving hostname...", "info")
        try:
            hostname = self.parsed.netloc.split(':')[0]
            ip = socket.gethostbyname(hostname)
            self.results['domain_info']['ip'] = ip
            log_emit(self.sid, f"IP address: {ip}", "success")
        except:
            self.results['domain_info']['ip'] = "Unknown"
            log_emit(self.sid, "DNS resolution failed", "warning")

        log_emit(self.sid, "Fetching server headers...", "info")
        try:
            resp = self.session.head(self.base_url, timeout=10, allow_redirects=True)
            server = resp.headers.get('Server', 'Unknown')
            self.results['server'] = {
                'server': server,
                'x_powered_by': resp.headers.get('X-Powered-By', 'Unknown'),
                'protocol': resp.url.split(':')[0],
                'status_code': resp.status_code,
                'content_type': resp.headers.get('Content-Type', 'Unknown'),
            }
            log_emit(self.sid, f"Server: {server}", "success")
        except Exception as e:
            log_emit(self.sid, f"Error retrieving headers: {e}", "error")
        self.delay()

        if self.parsed.scheme == 'https':
            log_emit(self.sid, "Checking SSL certificate...", "info")
            try:
                ctx = ssl.create_default_context()
                hostname = self.parsed.netloc.split(':')[0]
                with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                    s.settimeout(5)
                    s.connect((hostname, 443))
                    cert = s.getpeercert()
                    expiry = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    self.results['ssl'] = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'expires': expiry.strftime('%Y-%m-%d %H:%M:%S'),
                        'expired': expiry < datetime.now(),
                        'version': cert.get('version'),
                    }
                    log_emit(self.sid, f"Certificate valid until {expiry}", "success")
            except Exception as e:
                self.results['ssl'] = {'error': str(e)}
                log_emit(self.sid, f"SSL error: {e}", "warning")
        self.delay()

    def _fetch_homepage(self):
        self._step("Fetching homepage (with JS rendering if needed)...")
        html = get_rendered_html(self.base_url, self.session, self.sid)
        if not html:
            return
        self.results['homepage_size'] = len(html)
        soup = BeautifulSoup(html, 'html.parser')

        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.results['emails'] = list(set(re.findall(email_pattern, html)))
        if self.results['emails']:
            self.scores['data_exposure'] += 5

        social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com',
                          't.me', 'youtube.com', 'github.com']
        for a in soup.find_all('a', href=True):
            href = a['href']
            for sd in social_domains:
                if sd in href:
                    self.results['social'].append(href)
        self.results['social'] = list(set(self.results['social']))

        forms = []
        for form in soup.find_all('form'):
            action = form.get('action', '')
            method = form.get('method', 'GET').upper()
            inputs = [inp.get('name') for inp in form.find_all('input') if inp.get('name')]
            forms.append({'action': action, 'method': method, 'inputs': inputs})
        self.results['forms'] = forms

        comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
        self.results['html_comments'] = [c.strip() for c in comments if len(c.strip()) > 10]

        scripts = soup.find_all('script')
        inline_scripts = [s.text for s in scripts if s.text.strip()]
        all_text = html + ' '.join(inline_scripts)

        candidate_urls = re.findall(r'''["']([^"']*(?:api|ajax|rest|graphql|comments|posts|users)[^"']*)["']''',
                                    all_text, re.I)
        full_urls = set()
        for u in candidate_urls:
            if u.startswith('http'):
                full_urls.add(u)
            else:
                full_urls.add(urljoin(self.base_url, u))
        candidate_paths = re.findall(r'''["'](/[^"']*\b(?:api|ajax|rest|graphql|comments|posts|users)\b[^"']*)["']''',
                                     all_text, re.I)
        full_urls.update([urljoin(self.base_url, p) for p in candidate_paths])
        for f in forms:
            if f['action']:
                full_urls.add(urljoin(self.base_url, f['action']))
        for fname in ['robots.txt', 'sitemap.xml']:
            full_urls.add(urljoin(self.base_url, fname))
        self.results['endpoints'] = list(full_urls)[:50]
        log_emit(self.sid, f"Homepage analyzed. {len(self.results['endpoints'])} endpoints found.", "success")

    def _check_common_endpoints(self):
        self._step("Checking common directories and sensitive files...")
        for path in COMMON_DIRS + SENSITIVE_FILES:
            url = urljoin(self.base_url, path)
            try:
                r = self.session.get(url, timeout=5, allow_redirects=False)
                if r.status_code == 200:
                    self.results['interesting_files'].append({'url': url, 'status': r.status_code})
                    log_emit(self.sid, f"Found {url} (HTTP 200)", "warning")
                    self.scores['security'] -= 2
                if 'Index of /' in r.text and path.endswith('/'):
                    self.results['directory_listing'].append(url)
                    log_emit(self.sid, f"Directory listing: {url}", "error")
                    self.scores['security'] -= 5
            except:
                pass
            self.delay()
        log_emit(self.sid, "Path scanning complete.", "success")

    def _vulnerability_checks(self):
        self._step("Running security checks...")
        try:
            r = self.session.get(self.base_url, timeout=10)
            headers = r.headers
            sec = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not set'),
                'X-Frame-Options': headers.get('X-Frame-Options', 'Not set'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not set'),
                'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not set'),
                'X-XSS-Protection': headers.get('X-XSS-Protection', 'Not set'),
            }
            self.results['security_headers'] = sec
            for h, v in sec.items():
                if v == 'Not set':
                    self.results['vulnerabilities'].append(f"Missing security header: {h}")
                    log_emit(self.sid, f"Missing header {h}", "warning")
                    self.scores['security'] -= 5
        except:
            pass
        self.delay()

        log_emit(self.sid, "Testing CORS configuration...", "info")
        try:
            test_origin = "http://evil.example.com"
            r = self.session.get(self.base_url, headers={'Origin': test_origin}, timeout=10)
            acao = r.headers.get('Access-Control-Allow-Origin', '')
            if acao == '*' or acao == test_origin:
                self.results['vulnerabilities'].append(f"Overly permissive CORS: {acao}")
                log_emit(self.sid, f"CORS vulnerability: {acao}", "error")
                self.scores['security'] -= 15
        except:
            pass
        self.delay()

    def _id_hunting(self):
        self._step("Hunting numeric IDs in endpoints...")
        endpoints_to_test = self.results['endpoints'][:]
        common_patterns = ['/ajax', '/api', '/wp-admin/admin-ajax.php', '/rest/comments', '/graphql']
        for cp in common_patterns:
            full = urljoin(self.base_url, cp)
            if full not in endpoints_to_test:
                endpoints_to_test.append(full)

        total_tested = 0
        success_tested = 0
        for ep in endpoints_to_test[:25]:
            log_emit(self.sid, f"Probing endpoint: {ep}", "info")
            methods = ['GET']
            if 'ajax' in ep or 'api' in ep:
                methods.append('POST')
            for method in methods:
                try:
                    if method == 'POST':
                        for action in COMMON_ACTION_NAMES[:3]:
                            payload = {'action': action}
                            r = self.session.post(ep, json=payload, timeout=10)
                            total_tested += 1
                            if self._analyze_response(r, ep, method, payload):
                                success_tested += 1
                            self.delay()
                            r = self.session.post(ep, data=payload, timeout=10)
                            if self._analyze_response(r, ep, method, payload):
                                success_tested += 1
                            self.delay()
                    else:
                        r = self.session.get(ep, timeout=10)
                        total_tested += 1
                        if self._analyze_response(r, ep, method, None):
                            success_tested += 1
                except:
                    pass
                self.delay()
        if total_tested > 0:
            success_rate = (success_tested / total_tested) * 100
            self.scores['data_exposure'] += success_rate / 10

    def _analyze_response(self, response, url, method, data):
        content_type = response.headers.get('Content-Type', '')
        if 'json' in content_type or response.text.strip().startswith(('{', '[')):
            try:
                json_data = response.json()
                self._find_ids_in_json(json_data, url, method, data)
                return True
            except:
                pass
        return False

    def _find_ids_in_json(self, data, url, method, data_sent, depth=0):
        if depth > 5:
            return
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, int) and 'id' in key.lower():
                    self.results['id_analysis'].append({
                        'url': url,
                        'method': method,
                        'key': key,
                        'value': value,
                        'type': 'single_id',
                        'classification': 'user' if 'user' in key else 'content',
                        'characteristics': {
                            'length': len(str(value)),
                            'numeric': True,
                            'fixed_length': False,
                            'entropy': entropy([value])
                        }
                    })
                if isinstance(value, list) and len(value) > 0 and all(isinstance(i, dict) for i in value):
                    ids = []
                    for obj in value:
                        for k, v in obj.items():
                            if 'id' in k.lower() and isinstance(v, int):
                                ids.append(v)
                    if ids:
                        ids.sort()
                        lengths = [len(str(i)) for i in ids]
                        fixed_length = len(set(lengths)) == 1
                        ent = entropy(ids)
                        gaps = np.diff(ids).astype(int) if len(ids) > 1 else np.array([], dtype=int)
                        avg_gap = np.mean(gaps) if len(gaps) > 0 else 0
                        median_gap = np.median(gaps) if len(gaps) > 0 else 0
                        max_gap = np.max(gaps) if len(gaps) > 0 else 0
                        sequential = (ids == list(range(ids[0], ids[-1]+1)))
                        estimate = None
                        if sequential and ids[0] <= 2:
                            estimate = ids[-1]
                        if not self.growth_data and estimate is not None:
                            self.growth_data.append((datetime.now(), estimate))
                        reliab = 100
                        if not sequential:
                            reliab -= 30
                        if avg_gap > 10:
                            reliab -= 20
                        if ent > 0.8:
                            reliab -= 20
                        if not fixed_length:
                            reliab -= 10
                        reliab = max(0, reliab)
                        self.scores['id_reliability'] = max(self.scores['id_reliability'], reliab)
                        self.results['id_analysis'].append({
                            'url': url,
                            'method': method,
                            'field': 'multiple_ids',
                            'ids': ids[:50],
                            'total_found': len(value),
                            'min': ids[0],
                            'max': ids[-1],
                            'count': len(ids),
                            'sequential': sequential,
                            'estimate_total_users': estimate,
                            'characteristics': {
                                'fixed_length': fixed_length,
                                'length_distribution': {l: lengths.count(l) for l in set(lengths)},
                                'entropy': round(ent, 3),
                                'gap_analysis': {
                                    'average': round(avg_gap, 1),
                                    'median': round(median_gap, 1),
                                    'max_gap': int(max_gap)
                                }
                            },
                            'classification': classify_endpoint(url)
                        })
                        log_emit(self.sid, f"ID array found: {len(value)} objects, range {ids[0]}-{ids[-1]}", "success")
                self._find_ids_in_json(value, url, method, data_sent, depth+1)
        elif isinstance(data, list):
            for item in data:
                self._find_ids_in_json(item, url, method, data_sent, depth+1)

    def _finalize(self):
        self._step("Finalizing results...")
        self.results['id_analysis'] = [dict(t) for t in {tuple(d.items()) for d in self.results['id_analysis']}]
        self.scores['security'] = max(0, min(100, self.scores['security']))
        self.scores['data_exposure'] = min(100, self.scores['data_exposure'])
        self.scores['id_reliability'] = max(0, min(100, self.scores['id_reliability']))
        log_emit(self.sid, "Analysis complete.", "success")

    def start_monitoring(self, endpoint, method, data_str, interval_seconds=3600):
        if self.monitoring_active:
            return False
        self.monitoring_active = True
        data = json.loads(data_str) if data_str else {}
        def monitor():
            last_max = None
            while self.monitoring_active:
                try:
                    if method == 'POST':
                        r = self.session.post(endpoint, json=data, timeout=15)
                    else:
                        r = self.session.get(endpoint, timeout=15)
                    if r.headers.get('Content-Type', '').startswith('application/json'):
                        json_data = r.json()
                        def extract_max(js, depth=0):
                            if depth > 3: return None
                            if isinstance(js, list) and all(isinstance(i, dict) for i in js):
                                ids = [v for obj in js for k, v in obj.items() if 'id' in k.lower() and isinstance(v, int)]
                                if ids: return max(ids)
                            if isinstance(js, dict):
                                for k, v in js.items():
                                    if isinstance(v, list) and all(isinstance(i, dict) for i in v):
                                        ids = [v2 for obj in v for k2, v2 in obj.items() if 'id' in k2.lower() and isinstance(v2, int)]
                                        if ids: return max(ids)
                                    if isinstance(v, (dict, list)):
                                        res = extract_max(v, depth+1)
                                        if res: return res
                            return None
                        current_max = extract_max(json_data)
                        if current_max is not None:
                            now = datetime.now()
                            self.growth_data.append((now, current_max))
                            if len(self.growth_data) > 20:
                                self.growth_data.pop(0)
                            slope = None
                            prediction = None
                            if len(self.growth_data) >= 2:
                                times = [(t - self.growth_data[0][0]).total_seconds() / 3600 for t, _ in self.growth_data]
                                vals = [v for _, v in self.growth_data]
                                slope, intercept = np.polyfit(times, vals, 1)
                                next_time = times[-1] + (interval_seconds / 3600)
                                prediction = int(round(slope * next_time + intercept))
                            emit_data = {
                                'time': now.strftime('%H:%M:%S'),
                                'max_id': current_max,
                                'slope_per_hour': round(slope, 1) if slope is not None else None,
                                'predicted_next': prediction
                            }
                            from core.utils import _socketio
                            if _socketio:
                                _socketio.emit('monitor_update', emit_data, room=self.sid)
                except Exception as e:
                    from core.utils import _socketio
                    if _socketio:
                        _socketio.emit('log', {'msg': f"Monitor error: {e}", 'level': 'error'}, room=self.sid)
                time.sleep(interval_seconds)
        self.monitor_thread = threading.Thread(target=monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        return True

    def stop_monitoring(self):
        self.monitoring_active = False