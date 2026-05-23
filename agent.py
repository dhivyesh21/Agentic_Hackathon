# agent.py
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "status":              {"type": "string", "enum": ["SAFE", "UNDER ATTACK"]},
        "attack_type":         {"type": "string"},
        "severity":            {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"]},
        "attacker_ip":         {"type": "string"},
        "confidence_score":    {"type": "number"},
        "affected_endpoints":  {"type": "array", "items": {"type": "string"}},
        "ioc_tags":            {"type": "array", "items": {"type": "string"}},
        "payload_explanation": {"type": "array", "items": {"type": "string"}},                     
        "summary":             {"type": "string"},
        "recommended_action":  {"type": "string"},
        "mitre_tactic":        {"type": "string"},
    },
    "required": [
        "status", "attack_type", "severity", "attacker_ip",
        "confidence_score", "affected_endpoints", "ioc_tags",
        "payload_explanation", "summary", "recommended_action", "mitre_tactic"
    ]
}

_SIMULATION_SCHEMA = {
    "type": "object",
    "properties": {
        "kill_chain_stages":    {"type": "array", "items": {"type": "string"}},
        "blast_radius":         {"type": "string"},
        "dwell_time_estimate":  {"type": "string"},
        "next_likely_move":     {"type": "string"},
    },
    "required": ["kill_chain_stages", "blast_radius", "dwell_time_estimate", "next_likely_move"]
}

_ANALYSIS_RULES = (
    "You are an elite Autonomous Incident Response Agent operating inside a Tier-1 SOC.\n"
    "Analyze the incoming raw log stream and produce a structured forensic threat report.\n\n"
    "Rules:\n"
    "- status: 'SAFE' if no threat, 'UNDER ATTACK' if any malicious pattern is confirmed.\n"
    "- attack_type: A concise threat profile label (e.g. 'SQL Injection', 'Brute-Force', 'XSS', 'C2 Beacon'). Use 'None' if SAFE.\n"
    "- severity: 'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL' based on impact potential.\n"
    "- attacker_ip: The source IP of the threat actor. Use 'None' if SAFE.\n"
    "- confidence_score: A float from 0.0 to 1.0 representing your confidence in the threat classification.\n"
    "- affected_endpoints: A list of URL paths or services targeted in the logs.\n"
    "- ioc_tags: Short Indicators of Compromise tags extracted from the logs (e.g. 'root_bypass', 'data_exfil', 'auth_flood').\n"
    "- payload_explanation: If malicious payloads, exploit syntax, suspicious PowerShell commands, SQL injections, or attack code are detected, return a JSON array of SHORT bullet-point explanations. "
    "Each bullet must explain ONE malicious behavior in simple cybersecurity language. "
    "Keep explanations concise and readable for non-technical analysts. "
    "Maximum 5 bullet points. "
    "Do NOT generate paragraphs. "
    "Do NOT use markdown. "
    "Do NOT use arrows, symbols, or special characters. "
    "If no exploit syntax exists, return an empty array [].\n"
    "- summary: A concise high-level narrative of the threat actor's behavior and objective.\n"
    "- recommended_action: A direct, actionable mitigation directive (e.g. 'Block IP 203.0.113.88 at perimeter firewall, terminate session root_bypass, rotate all credentials').\n"
    "- mitre_tactic: The most relevant MITRE ATT&CK tactic name (e.g. 'Credential Access', 'Initial Access', 'Exfiltration'). Use 'None' if SAFE.\n\n"
    "You MUST return every field listed in the schema. Never omit ioc_tags, affected_endpoints, or any required field.\n"
    "Output ONLY a valid JSON object. No preamble, no markdown fences."
)

_SIMULATION_RULES = (
    "You are a red-team simulation engine. Given a scenario name and its log trace, "
    "produce a concise attack simulation report detailing the strategic progression of the attack vector.\n"
    "You MUST return all four fields: kill_chain_stages, blast_radius, dwell_time_estimate, next_likely_move.\n"
    "kill_chain_stages must always be a non-empty array of strings.\n"
    "Output ONLY valid JSON. No markdown, no preamble."
)


def _build_client() -> genai.Client:
    return genai.Client()


def _safe_parse(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _enforce_defaults(report: dict) -> dict:
    report.setdefault("status", "SAFE")
    report.setdefault("attack_type", "None")
    report.setdefault("severity", "LOW")
    report.setdefault("attacker_ip", "None")
    report.setdefault("confidence_score", 0.0)
    report.setdefault("affected_endpoints", [])
    report.setdefault("ioc_tags", [])
    report.setdefault("payload_explanation", [])
    report.setdefault("summary", "No anomalies detected.")
    report.setdefault("recommended_action", "None")
    report.setdefault("mitre_tactic", "None")
    if not isinstance(report["affected_endpoints"], list):
        report["affected_endpoints"] = []
    if not isinstance(report["ioc_tags"], list):
        report["ioc_tags"] = []
    return report


def analyze_incident_stream(logs: str) -> dict:
    client = _build_client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=logs,
        config=types.GenerateContentConfig(
            system_instruction=_ANALYSIS_RULES,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=_ANALYSIS_SCHEMA,
        ),
    )

    report = _safe_parse(response.text)

    if "payload_explanation" in report and isinstance(report["payload_explanation"], list):
        cleaned_payloads = []
        for item in report["payload_explanation"]:
            item = str(item)
            item = item.replace("arrow down", "")
            item = item.replace("Arrow Down", "")
            item = item.replace("↓", "")
            item = item.replace("➜", "")
            item = item.replace("➡", "")
            item = item.replace("->", "")
            item = item.strip()
            if item:
                cleaned_payloads.append(item)
        report["payload_explanation"] = cleaned_payloads

    return _enforce_defaults(report)


def investigate_threat_context(logs: str, question: str, history: list[dict] | None = None) -> str:
    client = _build_client()

    system_rules = (
        f"You are a helpful, conversational forensic security analyst investigating these logs:\n\n{logs}\n\n"
        "Instructions:\n"
        "1. For regular conversation, greetings, or pleasantries (e.g., 'thank you', 'hello', 'good job'), "
        "respond naturally, politely, and briefly as a helpful peer.\n"
        "2. For specific technical questions about the security incident, answer using objective evidence from the logs. "
        "Be direct, technically precise, and concise. Use bullet points for listing multiple findings.\n"
        "3. If asked how an attack was solved or mitigated, explain that the dashboard's Firewall Orchestration "
        "sub-system mitigates it by blocking the attacker's IP address at the perimeter firewall."
    )

    messages = []
    if history:
        for turn in history:
            api_role = "model" if turn["role"] == "assistant" else "user"
            messages.append({"role": api_role, "parts": [{"text": turn["content"]}]})
            
    messages.append({"role": "user", "parts": [{"text": question}]})

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_rules,
            temperature=0.2,
        ),
    )
    return response.text


def simulate_attack_vector(scenario_name: str, logs: str):
    client = _build_client()
    prompt = f"Scenario: {scenario_name}\n\nLogs:\n{logs}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_SIMULATION_RULES,
                temperature=0.3,
                response_mime_type="application/json",
                response_schema=_SIMULATION_SCHEMA,
            ),
        )
        sim = _safe_parse(response.text)
        sim.setdefault("kill_chain_stages", [])
        sim.setdefault("blast_radius", "Unknown")
        sim.setdefault("dwell_time_estimate", "Unknown")
        sim.setdefault("next_likely_move", "Unknown")
        if not isinstance(sim["kill_chain_stages"], list):
            sim["kill_chain_stages"] = []
        return sim
        
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return "⚠️ The simulation engine is cooling down due to API rate limits. Please wait 15-30 seconds and click 'Run Attack Simulation' again!"
        return f"Simulation engine connection error: {str(e)}"