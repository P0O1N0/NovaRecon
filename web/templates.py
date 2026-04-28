HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NovaRecon | Advanced Web Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@300;400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #050508;
            --bg-panel: #0d0d14;
            --bg-card: rgba(18, 18, 28, 0.7);
            --border-color: rgba(0, 229, 255, 0.15);
            --cyber-cyan: #00e5ff;
            --cyber-blue: #0077ff;
            --cyber-purple: #b026ff;
            --text-bright: #ffffff;
            --text-normal: #c7c7d4;
            --text-muted: #8b8b9e;
            --success: #00ff88;
            --warning: #ffb800;
            --danger: #ff3366;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: var(--bg-dark);
            background-image: 
                linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
            color: var(--text-normal);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }

        h1, h2, h3, h4, h5, h6, .cyber-font {
            font-family: 'Rajdhani', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-bright);
        }

        /* Navbar & Logo */
        .navbar {
            background: rgba(5, 5, 8, 0.9) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 0;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }
        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }
        .logo-text {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 1.8rem;
            letter-spacing: 2px;
            background: linear-gradient(90deg, var(--text-bright), var(--cyber-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .version-badge {
            background: rgba(0, 229, 255, 0.1);
            color: var(--cyber-cyan);
            border: 1px solid var(--cyber-cyan);
            font-family: 'Fira Code', monospace;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
        }

        /* Cyber Cards */
        .cyber-card {
            background: var(--bg-card);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .cyber-card::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--border-color), transparent);
            transition: all 0.3s ease;
        }
        .cyber-card:hover {
            border-color: rgba(0, 229, 255, 0.4);
            box-shadow: 0 8px 32px rgba(0, 229, 255, 0.1);
            transform: translateY(-2px);
        }
        .cyber-card:hover::before {
            background: linear-gradient(90deg, transparent, var(--cyber-cyan), transparent);
        }

        /* Input Area */
        .input-label {
            color: var(--text-bright);
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }
        .cyber-input-group {
            display: flex;
            background: var(--bg-panel);
            border: 1px solid rgba(0, 229, 255, 0.3);
            border-radius: 6px;
            padding: 6px;
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 229, 255, 0.05);
            transition: all 0.3s;
        }
        .cyber-input-group:focus-within {
            border-color: var(--cyber-cyan);
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 229, 255, 0.2);
        }
        .target-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 15px;
            color: var(--cyber-cyan);
            font-size: 1.2rem;
        }
        .cyber-input-group input {
            background: transparent;
            border: none;
            color: var(--text-bright);
            padding: 12px 10px;
            font-size: 1.1rem;
            flex-grow: 1;
            outline: none;
            font-family: 'Fira Code', monospace;
        }
        .cyber-input-group input::placeholder {
            color: #636378;
        }
        .btn-cyber {
            background: linear-gradient(45deg, var(--cyber-blue), var(--cyber-cyan));
            border: none;
            color: #000;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 0 30px;
            border-radius: 4px;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
        }
        .btn-cyber:hover:not(:disabled) {
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
            transform: scale(1.02);
            color: #fff;
        }
        .btn-cyber:disabled {
            background: #2a2a35;
            color: #555;
            cursor: not-allowed;
        }

        /* Progress Panel (Replaces Overlay) */
        .progress-panel {
            background: var(--bg-panel);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 15px 20px;
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.4s ease-out;
        }
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .progress-status {
            color: var(--cyber-cyan);
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
        }
        .progress-percent {
            color: var(--text-bright);
            font-weight: 700;
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.2rem;
        }
        .cyber-progress-track {
            height: 6px;
            background: #1a1a24;
            border-radius: 3px;
            overflow: hidden;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.8);
        }
        .cyber-progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--cyber-purple), var(--cyber-cyan));
            box-shadow: 0 0 10px var(--cyber-cyan);
            transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        .cyber-progress-fill::after {
            content: '';
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shimmer 1.5s infinite;
        }
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        /* Terminal */
        .terminal-container {
            background: #09090d;
            border: 1px solid #1f1f2e;
            border-radius: 6px;
            margin-top: 20px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        }
        .terminal-header {
            background: #111118;
            padding: 8px 15px;
            border-bottom: 1px solid #1f1f2e;
            display: flex;
            align-items: center;
            border-radius: 6px 6px 0 0;
        }
        .terminal-title {
            color: #636378;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            margin-left: 10px;
        }
        .terminal-body {
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            padding: 15px;
            height: 250px;
            overflow-y: auto;
            color: var(--text-normal);
            line-height: 1.6;
        }

        /* Score Circles */
        .score-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .score-circle {
            width: 100px; height: 100px;
            border-radius: 50%;
            background: conic-gradient(var(--ring-color) calc(var(--score) * 1%), #1a1a24 0);
            display: flex; align-items: center; justify-content: center;
            position: relative;
            margin-top: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .score-circle::before {
            content: '';
            position: absolute;
            width: 86px; height: 86px;
            background: var(--bg-card);
            border-radius: 50%;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
        }
        .score-value {
            position: relative;
            font-family: 'Rajdhani', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-bright);
        }

        /* Lists & Data Presentation */
        .data-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px dashed rgba(255,255,255,0.05);
        }
        .data-row:last-child { border-bottom: none; }
        .data-label { color: var(--text-muted); font-size: 0.9rem; }
        .data-value { color: var(--text-bright); font-family: 'Fira Code', monospace; font-size: 0.9rem; text-align: right;}
        
        .vuln-item {
            background: rgba(255, 184, 0, 0.05);
            border-left: 3px solid var(--warning);
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
            color: var(--text-bright);
            font-size: 0.9rem;
        }
        .id-item {
            background: rgba(0, 229, 255, 0.03);
            border: 1px solid rgba(0, 229, 255, 0.1);
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 15px;
        }

        /* Form elements for Monitor */
        .cyber-input-sm {
            background: rgba(10, 10, 15, 0.8);
            border: 1px solid #2a2a35;
            color: var(--text-bright);
            border-radius: 4px;
            padding: 8px 12px;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            width: 100%;
            transition: border-color 0.3s;
        }
        .cyber-input-sm:focus { border-color: var(--cyber-cyan); outline: none; }
        .cyber-select {
            background: rgba(10, 10, 15, 0.8);
            border: 1px solid #2a2a35;
            color: var(--text-bright);
            border-radius: 4px;
            padding: 8px;
            width: 100%;
        }

        /* Animations */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        .fade-in { animation: fadeIn 0.5s ease-out forwards; opacity: 0; }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: #2a2a35; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--cyber-cyan); }

        /* Utility */
        .text-cyan { color: var(--cyber-cyan); }
        .text-purple { color: var(--cyber-purple); }

        /* Footer author tag */
        .cyber-footer {
            margin-top: auto;
            padding: 1.5rem 0 1rem;
            text-align: center;
            border-top: 1px solid rgba(0, 229, 255, 0.1);
        }
        .cyber-footer small {
            color: var(--text-muted);
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
        }
        .cyber-footer a {
            color: var(--cyber-cyan);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }
        .cyber-footer a:hover {
            text-shadow: 0 0 8px var(--cyber-cyan);
            text-decoration: underline;
        }
    </style>
</head>
<body>

<nav class="navbar sticky-top">
    <div class="container">
        <a class="logo-container" href="#">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="url(#cyber-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <defs>
                    <linearGradient id="cyber-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#00e5ff" />
                        <stop offset="100%" stop-color="#b026ff" />
                    </linearGradient>
                </defs>
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
                <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            <span class="logo-text">NOVARECON</span>
        </a>
        <div>
            <span class="badge version-badge px-3 py-2 rounded-pill">v3.0_CORE</span>
        </div>
    </div>
</nav>

<div class="container mt-5 mb-5">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="cyber-card p-4 p-md-5">
                <div>
                    <label class="input-label"><i class="fa-solid fa-satellite-dish me-2 text-cyan"></i>TARGET SPECIFICATION</label>
                    <div class="cyber-input-group">
                        <div class="target-icon">
                            <i class="fa-solid fa-crosshairs"></i>
                        </div>
                        <input type="text" id="domainInput" placeholder="Enter target domain (e.g. target.com)" autocomplete="off">
                        <button class="btn-cyber" id="startScan">INITIATE</button>
                    </div>
                </div>

                <div class="progress-panel" id="progressPanel">
                    <div class="progress-header">
                        <div class="progress-status" id="scanStatus"><i class="fa-solid fa-circle-notch fa-spin me-2"></i>Establishing connection...</div>
                        <div class="progress-percent" id="progressPercent">0%</div>
                    </div>
                    <div class="cyber-progress-track">
                        <div class="cyber-progress-fill" id="progressBar"></div>
                    </div>
                </div>

                <div class="terminal-container">
                    <div class="terminal-header">
                        <i class="fa-solid fa-terminal text-cyan" style="font-size: 0.8rem;"></i>
                        <span class="terminal-title">nova-recon@system:~/scanner$</span>
                    </div>
                    <div class="terminal-body" id="logContainer">
                        <span style="color: #636378;">[SYS] Ready for target acquisition. Awaiting user input...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="resultsArea" class="mt-5" style="display: none;">
        <div class="row g-4 mb-4">
            <div class="col-md-4 fade-in" style="animation-delay: 0.1s">
                <div class="cyber-card p-4 h-100 score-box">
                    <h6 class="cyber-font text-cyan mb-0">Security Score</h6>
                    <div class="score-circle" id="securityCircle" style="--ring-color: var(--cyber-cyan);">
                        <span class="score-value" id="securityScore">0</span>
                    </div>
                </div>
            </div>
            <div class="col-md-4 fade-in" style="animation-delay: 0.2s">
                <div class="cyber-card p-4 h-100 score-box">
                    <h6 class="cyber-font text-warning mb-0">Data Exposure</h6>
                    <div class="score-circle" id="exposureCircle" style="--ring-color: var(--warning);">
                        <span class="score-value" id="exposureScore">0</span>
                    </div>
                </div>
            </div>
            <div class="col-md-4 fade-in" style="animation-delay: 0.3s">
                <div class="cyber-card p-4 h-100 score-box">
                    <h6 class="cyber-font text-success mb-0">ID Reliability</h6>
                    <div class="score-circle" id="reliabilityCircle" style="--ring-color: var(--success);">
                        <span class="score-value" id="reliabilityScore">0</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-md-6 fade-in" style="animation-delay: 0.4s">
                <div class="cyber-card p-4 h-100">
                    <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-server me-2 text-cyan"></i>Infrastructure</h5>
                    <div id="domainInfo"></div>
                </div>
            </div>
            <div class="col-md-6 fade-in" style="animation-delay: 0.5s">
                <div class="cyber-card p-4 h-100">
                    <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-shield-haltered me-2 text-purple"></i>SSL & Cryptography</h5>
                    <div id="sslInfo"></div>
                </div>
            </div>
        </div>

        <div class="cyber-card p-4 mb-4 fade-in" style="animation-delay: 0.6s">
            <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-bug me-2 text-warning"></i>Vulnerability Assessment</h5>
            <div id="vulnList"></div>
        </div>

        <div class="cyber-card p-4 mb-4 fade-in" style="animation-delay: 0.7s">
            <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-fingerprint me-2 text-success"></i>ID Intelligence & Pattern Recognition</h5>
            <div id="idAnalysis"></div>
        </div>

        <div class="cyber-card p-4 mb-4 fade-in" style="animation-delay: 0.8s">
            <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-chart-line me-2 text-cyan"></i>Live Telemetry Monitor</h5>
            <div class="row g-3 align-items-end mb-4">
                <div class="col-md-3">
                    <label class="data-label mb-1">Target Endpoint</label>
                    <input type="text" id="monitorEndpoint" class="cyber-input-sm" placeholder="https://api...">
                </div>
                <div class="col-md-2">
                    <label class="data-label mb-1">Method</label>
                    <select id="monitorMethod" class="cyber-select">
                        <option value="GET">GET</option>
                        <option value="POST">POST</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="data-label mb-1">Payload (JSON)</label>
                    <input type="text" id="monitorData" class="cyber-input-sm" placeholder='{"id": 1}'>
                </div>
                <div class="col-md-2">
                    <label class="data-label mb-1">Interval (s)</label>
                    <input type="number" id="monitorInterval" class="cyber-input-sm" value="3600">
                </div>
                <div class="col-md-2 d-flex gap-2">
                    <button class="btn-cyber flex-fill px-0 text-center" id="startMonitor" style="font-size:0.9rem;" title="Deploy Monitor"><i class="fa-solid fa-play"></i></button>
                    <button class="btn-cyber flex-fill px-0 text-center" id="stopMonitor" style="background: var(--bg-panel); color: var(--danger); border: 1px solid var(--danger); font-size:0.9rem;" title="Halt Monitor"><i class="fa-solid fa-stop"></i></button>
                </div>
            </div>
            
            <div class="terminal-container" style="margin-top:0;">
                <div class="terminal-body" id="monitorLog" style="height: 150px; color: var(--text-muted);">
                    [MONITOR] Standing by...
                </div>
            </div>
        </div>

        <div class="cyber-card p-4 mb-4 fade-in" style="animation-delay: 0.9s">
            <h5 class="cyber-font mb-4 border-bottom border-secondary pb-2"><i class="fa-solid fa-link me-2 text-purple"></i>Discovered Assets</h5>
            <div id="endpointsData"></div>
        </div>
    </div>
</div>

<!-- Author footer – perfectly blended into the cyberpunk theme -->
<footer class="cyber-footer">
    <small>
        Author: <a href="https://t.me/P0O1N0" target="_blank" rel="noopener noreferrer">P0O1N0 <i class="fa-brands fa-telegram ms-1"></i></a>
    </small>
</footer>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
    const socket = io();
    const logDiv = document.getElementById('logContainer');
    const domainInput = document.getElementById('domainInput');
    const startBtn = document.getElementById('startScan');
    const progressPanel = document.getElementById('progressPanel');
    const progressBar = document.getElementById('progressBar');
    const scanStatus = document.getElementById('scanStatus');
    const progressPercent = document.getElementById('progressPercent');
    const resultsArea = document.getElementById('resultsArea');

    function log(msg, level='info') {
        const line = document.createElement('div');
        let color = 'var(--text-normal)';
        let prefix = '[*]';
        
        if (level === 'error') { color = 'var(--danger)'; prefix = '[-]'; }
        else if (level === 'warning') { color = 'var(--warning)'; prefix = '[!]'; }
        else if (level === 'success') { color = 'var(--success)'; prefix = '[+]'; }
        
        line.style.color = color;
        const time = new Date().toLocaleTimeString('en-US', {hour12: false, hour: "numeric", minute: "numeric", second: "numeric"});
        line.innerHTML = `<span style="color:#636378">[${time}]</span> ${prefix} ${msg}`;
        
        logDiv.appendChild(line);
        logDiv.scrollTop = logDiv.scrollHeight;
    }

    socket.on('log', data => log(data.msg, data.level));

    socket.on('progress', data => {
        progressPanel.style.display = 'block';
        progressBar.style.width = data.percent + '%';
        progressPercent.textContent = data.percent + '%';
        scanStatus.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin me-2"></i>${data.text}`;
    });

    socket.on('scan_complete', data => {
        scanStatus.innerHTML = `<i class="fa-solid fa-check text-success me-2"></i>Analysis Complete`;
        progressBar.style.width = '100%';
        progressPercent.textContent = '100%';
        
        setTimeout(() => {
            progressPanel.style.display = 'none';
            resultsArea.style.display = 'block';
        }, 1000);

        const r = data.results;
        const scores = data.scores;

        animateScore('securityScore', scores.security, 'securityCircle');
        animateScore('exposureScore', scores.data_exposure, 'exposureCircle');
        animateScore('reliabilityScore', scores.id_reliability, 'reliabilityCircle');

        // Server Info
        document.getElementById('domainInfo').innerHTML = `
            <div class="data-row"><span class="data-label">IP Address</span><span class="data-value">${r.domain_info.ip || 'Unknown'}</span></div>
            <div class="data-row"><span class="data-label">Server Tech</span><span class="data-value">${r.server.server || 'Unknown'}</span></div>
            <div class="data-row"><span class="data-label">X-Powered-By</span><span class="data-value">${r.server.x_powered_by || 'Unknown'}</span></div>
            <div class="data-row"><span class="data-label">Status Code</span><span class="data-value text-success">${r.server.status_code || '-'}</span></div>
        `;

        // SSL Info
        const ssl = r.ssl;
        if (ssl.error) {
            document.getElementById('sslInfo').innerHTML = `<div class="text-danger mt-3"><i class="fa-solid fa-triangle-exclamation me-2"></i>${ssl.error}</div>`;
        } else if (ssl.expires) {
            document.getElementById('sslInfo').innerHTML = `
                <div class="data-row"><span class="data-label">Certificate Status</span><span class="data-value">${ssl.expired ? '<span style="color:var(--danger)">EXPIRED</span>' : '<span style="color:var(--success)">VALID</span>'}</span></div>
                <div class="data-row"><span class="data-label">Expiry Date</span><span class="data-value">${ssl.expires}</span></div>
                <div class="data-row"><span class="data-label">Issuer Organization</span><span class="data-value">${ssl.issuer?.commonName || ssl.issuer?.organizationName || '-'}</span></div>
            `;
        } else {
            document.getElementById('sslInfo').innerHTML = '<div class="text-muted mt-3">Non-HTTPS or No SSL Certificate detected.</div>';
        }

        // Vulnerabilities
        let vulnHtml = '';
        if(r.vulnerabilities.length) {
            r.vulnerabilities.forEach(v => vulnHtml += `<div class="vuln-item"><i class="fa-solid fa-skull me-2"></i>${v}</div>`);
        }
        if (Object.keys(r.security_headers).length) {
            vulnHtml += '<h6 class="cyber-font text-cyan mt-4 mb-3">Security Headers Matrix</h6><div class="row g-2">';
            Object.entries(r.security_headers).forEach(([h, v]) => {
                let isMissing = v === 'Not set';
                vulnHtml += `
                <div class="col-md-6">
                    <div style="background:rgba(0,0,0,0.3); border:1px solid ${isMissing ? 'var(--danger)' : 'var(--success)'}; padding:8px 12px; border-radius:4px;">
                        <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">${h}</div>
                        <div style="font-size:0.85rem; font-family:'Fira Code', monospace; color:${isMissing ? 'var(--danger)' : 'var(--success)'}; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">${v}</div>
                    </div>
                </div>`;
            });
            vulnHtml += '</div>';
        }
        document.getElementById('vulnList').innerHTML = vulnHtml || '<div class="text-success"><i class="fa-solid fa-check me-2"></i>No major vulnerabilities detected.</div>';

        // IDs
        let idHtml = '';
        r.id_analysis.forEach(item => {
            if (item.type === 'single_id') {
                idHtml += `
                <div class="id-item d-flex justify-content-between align-items-center">
                    <div><i class="fa-solid fa-key text-cyan me-2"></i><code class="text-normal" style="background:transparent">${item.url}</code></div>
                    <div class="text-bright"><span class="text-muted">Key:</span> ${item.key} <span class="mx-2 text-cyan">➔</span> <span class="text-muted">Val:</span> ${item.value}</div>
                </div>`;
            } else {
                const chars = item.characteristics;
                let extra = '';
                if (chars) {
                    extra = `<span class="badge" style="background:rgba(255,255,255,0.1); color:var(--text-bright)">Entropy: ${chars.entropy}</span> <span class="badge" style="background:rgba(255,255,255,0.1); color:var(--text-bright)">Avg Gap: ~${chars.gap_analysis.average}</span>`;
                    if (!item.sequential && chars.gap_analysis.average > 100)
                        extra += ' <span class="badge bg-danger text-white"><i class="fa-solid fa-bolt"></i> High Randomization</span>';
                }
                idHtml += `
                <div class="id-item">
                    <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-secondary">
                        <div class="text-cyan font-monospace" style="font-size:0.9rem;"><i class="fa-solid fa-database me-2"></i>${item.url}</div>
                        <span class="badge border border-secondary text-muted" style="background:#1a1a24">${item.method}</span>
                    </div>
                    <div class="row g-2 text-normal" style="font-size:0.85rem;">
                        <div class="col-md-4"><span class="text-muted d-block">Classification</span>${item.classification.join(', ')}</div>
                        <div class="col-md-4"><span class="text-muted d-block">Data Range</span>Count: ${item.count} [${item.min} - ${item.max}]</div>
                        <div class="col-md-4"><span class="text-muted d-block">Pattern Sequence</span>${item.sequential ? '<span class="text-success">Sequential</span>' : '<span class="text-warning">Non-Sequential</span>'}</div>
                        <div class="col-12 mt-2 pt-2 border-top border-secondary d-flex gap-2 align-items-center">
                            ${extra}
                            ${item.estimate_total_users ? `<span class="ms-auto text-success" style="font-family:'Rajdhani',sans-serif; font-size:1.1rem;"><i class="fa-solid fa-users me-1"></i>Est. Records: ${item.estimate_total_users}</span>` : ''}
                        </div>
                    </div>
                </div>`;
            }
        });
        document.getElementById('idAnalysis').innerHTML = idHtml || '<div class="text-muted">No quantifiable numeric IDs mapped.</div>';

        // Endpoints
        let epHtml = '';
        if (r.endpoints.length) {
            epHtml += '<h6 class="cyber-font text-cyan mb-2">API / Routes</h6><div class="d-flex flex-wrap gap-2 mb-4">';
            r.endpoints.forEach(e => epHtml += `<span class="badge" style="background:rgba(0, 119, 255, 0.1); border:1px solid var(--cyber-blue); color:var(--text-bright); font-family:'Fira Code', monospace; font-weight:normal;">${e}</span>`);
            epHtml += '</div>';
        }
        if (r.emails.length) epHtml += `<h6 class="cyber-font text-cyan mb-2">Discovered Emails</h6><div class="mb-4 text-normal" style="font-family:'Fira Code', monospace">${r.emails.join(', ')}</div>`;
        if (r.social.length) epHtml += `<h6 class="cyber-font text-cyan mb-2">External Vectors (Social)</h6><div class="text-normal" style="font-family:'Fira Code', monospace">${r.social.join(', ')}</div>`;
        
        document.getElementById('endpointsData').innerHTML = epHtml || '<div class="text-muted">No external assets or routes mapped.</div>';

        log('Reconnaissance fully executed.', 'success');
        startBtn.disabled = false;
        startBtn.innerHTML = 'NEW SCAN';
    });

    function animateScore(elementId, target, circleId) {
        const el = document.getElementById(elementId);
        const circle = document.getElementById(circleId);
        let current = 0;
        const step = target / 30;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.round(current);
            circle.style.setProperty('--score', Math.round(current));
        }, 30);
    }

    startBtn.addEventListener('click', () => {
        const domain = domainInput.value.trim();
        if (!domain) {
            domainInput.style.borderColor = 'var(--danger)';
            setTimeout(() => domainInput.style.borderColor = '', 1000);
            return;
        }
        
        logDiv.innerHTML = '<span style="color: #636378;">[SYS] Clearing previous logs...</span>';
        resultsArea.style.display = 'none';
        
        progressPanel.style.display = 'block';
        progressBar.style.width = '0%';
        progressPercent.textContent = '0%';
        scanStatus.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin me-2"></i>Initializing scan sequence...`;
        
        socket.emit('start_scan', {domain: domain});
        log(`Target locked: ${domain}. Initiating scan sequence...`, 'info');
        
        startBtn.disabled = true;
        startBtn.innerHTML = 'SCANNING...';
    });

    document.getElementById('startMonitor').addEventListener('click', () => {
        const ep = document.getElementById('monitorEndpoint').value.trim();
        const method = document.getElementById('monitorMethod').value;
        const data = document.getElementById('monitorData').value.trim();
        const interval = parseInt(document.getElementById('monitorInterval').value) || 3600;
        socket.emit('start_monitor', {endpoint: ep, method: method, data: data, interval: interval});
        
        const mLog = document.getElementById('monitorLog');
        if(mLog.textContent.includes('Standing by')) mLog.innerHTML = '';
        mLog.innerHTML += `<div style="color: var(--success);"><i class="fa-solid fa-satellite-dish me-2"></i>Telemetry link established. Monitoring started.</div>`;
    });
    
    document.getElementById('stopMonitor').addEventListener('click', () => {
        socket.emit('stop_monitor');
        document.getElementById('monitorLog').innerHTML += `<div style="color: var(--danger);"><i class="fa-solid fa-link-slash me-2"></i>Telemetry link severed by user.</div>`;
    });
    
    socket.on('monitor_update', data => {
        const mLog = document.getElementById('monitorLog');
        let pred = data.predicted_next ? `<span class="text-cyan mx-2">➔</span> Next Est: <span class="text-bright">${data.predicted_next}</span>` : '';
        mLog.innerHTML += `<div><span style="color:#636378">[${data.time}]</span> Max ID: <span class="text-bright">${data.max_id}</span> <span class="text-purple mx-2">|</span> Rate: <span class="text-bright">${data.slope_per_hour}/h</span>${pred}</div>`;
        mLog.scrollTop = mLog.scrollHeight;
    });
    
    domainInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') startBtn.click();
    });
</script>
</body>
</html>
'''