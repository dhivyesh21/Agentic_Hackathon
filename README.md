# 🛡️ SentinelAI 

SentinelAI is a real-time, proactive cyber-defense platform designed to help security analysts outmaneuver threats. 
Instead of waiting for security teams to parse through thousands of messy, raw server log lines during a breach, our platform uses an intelligent 
backend pipeline to instantly structure the logs, predict the attacker's next move, and push automated firewall countermeasures to contain the incident in seconds.
---

# ⚡ Key Features

* **Live Log Stream Hooking:** Feeds raw server syslog arrays directly into an analytical engine.
* **Proactive Threat Modeler:** Reconstructs the attacker's progression step-by-step to calculate their system dwell time and predict their next target.
* **Forensic Payload Decoder:** Isolates targeted databases and translates complex exploit strings into plain-English summaries.
* **Firewall Orchestration Core:** Works in both Human-In-The-Loop and fully autonomous modes to push active blocking rules to edge routers.
* **Natural Language Threat Hunting:** A built-in workspace where responders can query the system memory using conversational questions.

---

## 🛠️ The Tech Stack

* **Frontend:** Streamlit (Custom Dark Matrix Theme)
* **AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Data Layer:** Strict Structured JSON Schema outputs
* **Environment:** Python (`dotenv` + stateful session runtimes)

---

## 👥 The Team

* **Dhivyesh P** — *Core Architecture & Interface Design*
* **Jetasri D K** — *Forensic Agent Logic & Infrastructure Backend*

Developed under pressure for the **Agentic Hackathon (2026)**. 🚀

---

## 🚀 How to Run It Locally

### 1. Grab the code
```bash
git clone [https://github.com/dhivyesh21/Agentic_Hackathon.git](https://github.com/dhivyesh21/Agentic_Hackathon.git)
cd Agentic_Hackathon
