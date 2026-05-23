# app.py
import sys
import importlib
import time
import streamlit as st

for _mod in ["agent", "mock_logs"]:
    if _mod in sys.modules:
        importlib.reload(sys.modules[_mod])

import mock_logs
import agent

st.set_page_config(
    page_title="SentinelAI // SOC Command",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg-deep:       #020b12;
    --bg-panel:      #04111c;
    --bg-card:       #061828;
    --border-dim:    #0d2d45;
    --border-glow:   #0ff;
    --accent-cyan:   #00e5ff;
    --accent-red:    #ff1744;
    --accent-green:  #00e676;
    --accent-amber:  #ffab00;
    --text-primary:  #e0f7fa;
    --text-muted:    #546e7a;
    --text-code:     #80cbc4;
    --font-mono:     'Share Tech Mono', monospace;
    --font-ui:       'Rajdhani', sans-serif;
    --font-body:     'Inter', sans-serif;
}

[data-testid="stSidebar"] button [class*="st-"] span,
[class*="st-emotion-cache"] svg,
.st-emotion-cache-1aeep0r,
[data-testid="stSidebarCollapseButton"] * {
    font-family: "Source Sans Pro", sans-serif !important;
}
            
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border-dim) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

h1, h2, h3, h4 {
    font-family: var(--font-ui) !important;
    letter-spacing: 0.08em;
    color: var(--accent-cyan) !important;
}

p, li, span, label, div {
    font-family: var(--font-body) !important;
}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
    font-family: var(--font-body) !important;
}

.st-emotion-cache-1aeep0r, [class*="st-"] svg, [data-testid="stExpander"] div[role="button"] span {
    font-family: "Source Sans Pro", sans-serif !important;
}

code, pre, [data-testid="stCode"] * {
    font-family: var(--font-mono) !important;
    background-color: #030f1a !important;
    color: var(--text-code) !important;
    border: 1px solid var(--border-dim) !important;
}

.sentinel-header {
    background: linear-gradient(135deg, #020b12 0%, #04172a 50%, #020b12 100%);
    border: 1px solid var(--border-dim);
    border-top: 2px solid var(--accent-cyan);
    border-radius: 4px;
    padding: 24px 32px 20px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.sentinel-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    animation: scanline 3s ease-in-out infinite;
}

@keyframes scanline {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}

.sentinel-title {
    font-family: var(--font-ui) !important;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent-cyan) !important;
    letter-spacing: 0.15em;
    margin: 0;
    text-shadow: 0 0 20px rgba(0,229,255,0.4);
}

.sentinel-sub {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem;
    color: var(--text-muted) !important;
    letter-spacing: 0.2em;
    margin-top: 4px;
}

.status-badge-attack {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,23,68,0.12);
    border: 1px solid var(--accent-red);
    border-radius: 3px;
    padding: 6px 14px;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem;
    color: var(--accent-red) !important;
    letter-spacing: 0.12em;
    animation: pulse-red 1.5s ease-in-out infinite;
}

.status-badge-safe {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,230,118,0.08);
    border: 1px solid var(--accent-green);
    border-radius: 3px;
    padding: 6px 14px;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem;
    color: var(--accent-green) !important;
    letter-spacing: 0.12em;
}

.status-badge-mitigated {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,229,255,0.08);
    border: 1px solid var(--accent-cyan);
    border-radius: 3px;
    padding: 6px 14px;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem;
    color: var(--accent-cyan) !important;
    letter-spacing: 0.12em;
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 6px rgba(255,23,68,0.3); }
    50% { box-shadow: 0 0 18px rgba(255,23,68,0.7); }
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-dim);
    border-radius: 4px;
    padding: 16px 20px;
    text-align: center;
}

.metric-label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    color: var(--text-muted) !important;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.metric-value {
    font-family: var(--font-ui) !important;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent-cyan) !important;
}

.metric-value-red   { color: var(--accent-red)   !important; }
.metric-value-green { color: var(--accent-green)  !important; }
.metric-value-amber { color: var(--accent-amber)  !important; }

.ioc-tag {
    display: inline-block;
    background: rgba(255,171,0,0.1);
    border: 1px solid rgba(255,171,0,0.4);
    border-radius: 2px;
    padding: 2px 10px;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem;
    color: var(--accent-amber) !important;
    margin: 2px 3px;
    letter-spacing: 0.1em;
}

.mitre-tag {
    display: inline-block;
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.3);
    border-radius: 2px;
    padding: 2px 10px;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem;
    color: var(--accent-cyan) !important;
    margin: 2px 3px;
    letter-spacing: 0.1em;
}

.kill-chain-step {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border-dim);
    font-family: var(--font-body) !important;
    font-size: 0.87rem;
    color: var(--text-primary) !important;
}

.kill-chain-num {
    font-family: var(--font-mono) !important;
    font-size: 0.7rem;
    color: var(--accent-amber) !important;
    background: rgba(255,171,0,0.1);
    border: 1px solid rgba(255,171,0,0.3);
    border-radius: 2px;
    padding: 1px 7px;
    white-space: nowrap;
    margin-top: 2px;
}

.section-label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem;
    color: var(--text-muted) !important;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border-dim);
}

.chat-bubble-user {
    background: rgba(0,229,255,0.06);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 4px 4px 4px 0;
    padding: 10px 16px;
    font-family: var(--font-body) !important;
    font-size: 0.88rem;
    color: var(--text-primary) !important;
    margin-bottom: 8px;
}

.chat-bubble-ai {
    background: rgba(4,17,28,0.9);
    border: 1px solid var(--border-dim);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 0 4px 4px 4px;
    padding: 10px 16px;
    font-family: var(--font-body) !important;
    font-size: 0.88rem;
    color: var(--text-primary) !important;
    margin-bottom: 8px;
}

.stButton > button {
    background: transparent !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    font-family: var(--font-ui) !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    border-radius: 3px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: rgba(0,229,255,0.1) !important;
    box-shadow: 0 0 16px rgba(0,229,255,0.25) !important;
}

.stButton > button[kind="primary"] {
    background: rgba(255,23,68,0.1) !important;
    border-color: var(--accent-red) !important;
    color: var(--accent-red) !important;
}

.stButton > button[kind="primary"]:hover {
    background: rgba(255,23,68,0.2) !important;
    box-shadow: 0 0 16px rgba(255,23,68,0.3) !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stToggle"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
}

[data-testid="stChatInput"] textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 10px rgba(0,229,255,0.15) !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 4px !important;
}

hr {
    border-color: var(--border-dim) !important;
    margin: 20px 0 !important;
}

.stSpinner > div {
    border-top-color: var(--accent-cyan) !important;
}

[data-testid="stAlert"] {
    border-radius: 3px !important;
    font-family: var(--font-body) !important;
}

.confidence-bar-wrap {
    background: var(--border-dim);
    border-radius: 2px;
    height: 6px;
    width: 100%;
    margin-top: 6px;
}

.confidence-bar-fill {
    height: 6px;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-amber));
    transition: width 0.8s ease;
}

.blocked-ip-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 12px;
    background: rgba(255,23,68,0.06);
    border: 1px solid rgba(255,23,68,0.2);
    border-radius: 3px;
    margin-bottom: 6px;
    font-family: var(--font-mono) !important;
    font-size: 0.75rem;
    color: var(--accent-red) !important;
}
</style>
""", unsafe_allow_html=True)


def _init_state():
    defaults = {
        "analysis_data":   None,
        "simulation_data": None,
        "chat_history":    [],
        "blocked_ips":     set(),
        "last_scenario":   None,
        "audit_ran":       False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


st.markdown("""
<div class="sentinel-header">
    <div class="sentinel-title">🛡 SENTINEL AI</div>
    <div class="sentinel-sub"> AUTONOMOUS SOC AGENT v2.0 &nbsp;|&nbsp; COGNITIVE DUO RUNTIME</div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<div class="section-label">⚡ Attack Simulation Engine</div>', unsafe_allow_html=True)
    selected_name = st.selectbox(
        "Traffic Profile Scenario",
        list(mock_logs.SCENARIOS.keys()),
        label_visibility="visible",
    )
    scenario_info = mock_logs.SCENARIOS[selected_name]
    st.caption(scenario_info["description"])

    st.divider()

    st.markdown('<div class="section-label">⚙ Agent Security Policy</div>', unsafe_allow_html=True)
    autonomous_mode = st.toggle("Fully Autonomous Mitigation", value=False)
    if autonomous_mode:
        st.warning("**IPS ACTIVE** — Agent will auto-block on detection.")
    else:
        st.info("**HITL MODE** — Human approval required before action.")

    st.divider()

    if st.session_state.blocked_ips:
        st.markdown('<div class="section-label">🔒 Firewall Blocklist</div>', unsafe_allow_html=True)
        for ip in sorted(st.session_state.blocked_ips):
            st.markdown(f'<div class="blocked-ip-row">⛔ {ip} — DROPPED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-label">🔒 Firewall Blocklist</div>', unsafe_allow_html=True)
        st.caption("No IPs currently blocked.")


if st.session_state.last_scenario != selected_name:
    st.session_state.analysis_data   = None
    st.session_state.simulation_data = None
    st.session_state.chat_history    = []
    st.session_state.audit_ran       = False
    st.session_state.last_scenario   = selected_name


st.markdown('<div class="section-label">📥 Raw Log Frame</div>', unsafe_allow_html=True)
st.code(scenario_info["logs"], language="bash")

run_col, sim_col = st.columns(2)
with run_col:
    audit_btn = st.button("🚀 Execute Forensic Audit", use_container_width=True)
with sim_col:
    sim_btn = st.button("⚔️ Run Attack Simulation", use_container_width=True)

if audit_btn:
    with st.spinner("Parsing logs against threat signatures..."):
        st.session_state.analysis_data = agent.analyze_incident_stream(scenario_info["logs"])
        st.session_state.chat_history  = []
        st.session_state.audit_ran     = True

if sim_btn:
    with st.spinner("Reconstructing attack kill chain..."):
        st.session_state.simulation_data = agent.simulate_attack_vector(
            selected_name, scenario_info["logs"]
        )

st.divider()

st.markdown('<div class="section-label">🤖 Agent Telemetry Diagnostics</div>', unsafe_allow_html=True)
report = st.session_state.analysis_data

if report:
    is_attack        = report.get("status") == "UNDER ATTACK"
    current_ip       = report.get("attacker_ip", "None")
    is_blocked       = current_ip in st.session_state.blocked_ips
    severity         = report.get("severity", "LOW")
    confidence       = report.get("confidence_score", 0.0)
    ioc_tags         = report.get("ioc_tags", [])
    mitre            = report.get("mitre_tactic", "None")
    endpoints        = report.get("affected_endpoints", [])

    sev_color = {
        "CRITICAL": "metric-value-red",
        "HIGH":     "metric-value-red",
        "MEDIUM":   "metric-value-amber",
        "LOW":      "metric-value-green",
    }.get(severity, "metric-value")
    if is_attack and is_blocked:
            st.markdown('<div class="status-badge-mitigated">● INCIDENT MITIGATED — FIREWALL ACTIVE</div>', unsafe_allow_html=True)
    elif is_attack and not is_blocked:
            st.markdown('<div class="status-badge-attack">● VECTOR COMPROMISE IDENTIFIED</div>', unsafe_allow_html=True)
    else:
            st.markdown('<div class="status-badge-safe">● ALL SYSTEMS NOMINAL</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Attack Type</div><div class="metric-value" style="font-size:1.1rem; padding: 4px 0;">{report.get("attack_type","None")}</div></div>', unsafe_allow_html=True)
    with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Severity</div><div class="metric-value {sev_color}">{severity}</div></div>', unsafe_allow_html=True)
    with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Attacker IP</div><div class="metric-value" style="font-size:1.2rem;">{current_ip}</div></div>', unsafe_allow_html=True)
    with m4:
            conf_pct = int(confidence * 100)
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Confidence</div>'
                f'<div class="metric-value">{conf_pct}%</div>'
                f'<div class="confidence-bar-wrap"><div class="confidence-bar-fill" style="width:{conf_pct}%"></div></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    tags_html = ""
    if mitre and mitre != "None":
            tags_html += f'<span class="mitre-tag">MITRE ATT&CK: {mitre}</span>'
    for tag in ioc_tags:
            tags_html += f'<span class="ioc-tag">{tag}</span>'
    if tags_html:
            st.markdown(f'<div style="line-height:2.2; margin-bottom: 15px;">{tags_html}</div>', unsafe_allow_html=True)

    if endpoints:
            st.markdown('<div class="section-label">Affected Endpoints</div>', unsafe_allow_html=True)
            ep_html = "".join(
                f'<code style="display:inline-block;margin:2px 4px;padding:2px 10px;'
                f'background:#030f1a;border:1px solid var(--border-dim);border-radius:2px;'
                f'font-family:var(--font-mono);font-size:0.75rem;color:var(--text-code)">{ep}</code>'
                for ep in endpoints
            )
            st.markdown(f'<div style="line-height:2.4; margin-bottom: 15px;">{ep_html}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-label">Incident Summary</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.88rem;color:var(--text-primary);line-height:1.6; margin-bottom: 20px;">{report.get("summary","")}</p>', unsafe_allow_html=True)

    payload_exp = report.get("payload_explanation", "None")
    if payload_exp and payload_exp.lower() != "none":
            with st.expander("🔎 Malicious Payload — Plain English Decoder", expanded=True):
                st.markdown(
                    f'<div style="font-family:var(--font-body);font-size:0.86rem;line-height:1.7;'
                    f'color:var(--text-primary);padding:4px 0">{payload_exp}</div>',
                    unsafe_allow_html=True,
                )

    if is_attack and is_blocked:
            st.success(f"🔒 Blacklist Rule Pushed: IP Address `{current_ip}` has been dropped at the perimeter firewall. Session terminated.")
            
    elif is_attack and not is_blocked:
            st.divider()
            st.markdown('<div class="section-label">🛡️ Response & Firewall Orchestration</div>', unsafe_allow_html=True)

            if autonomous_mode:
                st.session_state.blocked_ips.add(current_ip)
                st.rerun()
            else:
                st.info(f"**Proposed Directive:** {report.get('recommended_action','')}")
                approve_col, _ = st.columns([1, 1])
                with approve_col:
                    if st.button("✅ Approve & Execute Countermeasure", type="primary", use_container_width=True):
                        st.session_state.blocked_ips.add(current_ip)
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()

elif st.session_state.audit_ran:
    st.caption("Analysis returned no data. Retry the forensic audit.")
else:
    st.markdown(
        '<div style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted);'
        'padding:40px 20px;text-align:center;border:1px dashed var(--border-dim);border-radius:4px">'
        'AWAITING LOG STREAM &nbsp;—&nbsp; TRIGGER FORENSIC AUDIT TO POPULATE DASHBOARD'
        '</div>',
        unsafe_allow_html=True,
    )

st.divider()
st.markdown('<div class="section-label">🕵️ Forensic Threat Hunting — Natural Language Investigation</div>', unsafe_allow_html=True)

if report:
    for turn in st.session_state.chat_history:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])

    if user_query := st.chat_input("Investigate the logs (e.g. 'What was the first sign of compromise?')"):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            with st.spinner("Querying forensic memory layers..."):
                reply = agent.investigate_threat_context(
                    scenario_info["logs"],
                    user_query,
                    history=st.session_state.chat_history[:-1],
                )
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
else:
    st.markdown(
        '<div style="font-family:var(--font-mono);font-size:0.75rem;color:var(--text-muted);'
        'padding:20px;text-align:center;border:1px dashed var(--border-dim);border-radius:4px">'
        'RUN A FORENSIC AUDIT ABOVE TO UNLOCK THE THREAT HUNTING WORKSPACE'
        '</div>',
        unsafe_allow_html=True,
    )