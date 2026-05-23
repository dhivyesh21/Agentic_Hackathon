SCENARIOS = {
    "Standard Production Traffic": {
        "description": "🟢 Normal Activity: Safe, everyday employee and customer visits to the company website.",
        "logs": (
            "13:40:01 | INFO     | IP: 192.168.1.45   | Action: Opened Home Page        | Status: 200 SUCCESS\n"
            "13:40:15 | INFO     | IP: 172.16.5.102   | Action: User Logged In Securely | Status: 200 SUCCESS\n"
            "13:41:02 | INFO     | IP: 192.168.1.45   | Action: Loaded Website Images   | Status: 200 SUCCESS\n"
            "13:41:44 | INFO     | IP: 10.0.0.5       | Action: Checked System Health   | Status: 200 SUCCESS\n"
            "13:42:10 | INFO     | IP: 172.16.5.102   | Action: Loaded Dashboard Panel  | Status: 200 SUCCESS"
        ),
    },
    "Web Portal Brute-Force": {
        "description": "🟡 Brute-Force Attack: An automated script rapidly guessing user account passwords to hijack profiles.",
        "logs": (
            "13:42:11 | WARNING  | IP: 203.0.113.88   | Action: Login Attempt Failed    | Status: 401 UNAUTHORIZED (Try #1)\n"
            "13:42:12 | WARNING  | IP: 203.0.113.88   | Action: Login Attempt Failed    | Status: 401 UNAUTHORIZED (Try #2)\n"
            "13:42:13 | WARNING  | IP: 203.0.113.88   | Action: Login Attempt Failed    | Status: 401 UNAUTHORIZED (Try #3)\n"
            "13:42:14 | WARNING  | IP: 203.0.113.88   | Action: Login Attempt Failed    | Status: 401 UNAUTHORIZED (Try #4)\n"
            "13:42:15 | CRITICAL | IP: 203.0.113.88   | Action: Password Cracked!       | Status: 200 ROOT_ACCESS_GRANTED"
        ),
    },
    "SQL Injection Web Exploit": {
        "description": "🔴 SQL Injection: An attacker typing malicious database code into a text box to steal hidden customer records.",
        "logs": (
            "13:44:01 | WARNING  | IP: 198.51.100.12  | Input: ' OR '1'='1              | Status: 200 Bypass Check Executed\n"
            "13:44:05 | WARNING  | IP: 198.51.100.12  | Input: UNION SELECT credit_card | Status: 200 Database Rows Returned\n"
            "13:44:09 | WARNING  | IP: 198.51.100.12  | Input: DROP TABLE users;        | Status: 200 System Table Dropped\n"
            "13:44:12 | CRITICAL | IP: 198.51.100.12  | Action: Exporting Database Dump | Status: 200 EXFILTRATED (94 KB stolen)"
        ),
    },
    "XSS Stored Script Injection": {
        "description": "🟠 Cross-Site Scripting (XSS): Malicious code hidden inside a comment block to spy on real website visitors.",
        "logs": (
            "14:01:32 | WARNING  | IP: 45.33.32.156   | Comment: <script>steal.cookie()  | Status: 200 Malicious Script Planted\n"
            "14:01:45 | WARNING  | IP: 45.33.32.156   | Bio Box: <img onerror=hijack()>  | Status: 200 Spyware Injection Saved\n"
            "14:02:10 | CRITICAL | IP: 45.33.32.156   | Action: Stealing Admin Token    | Status: 200 SESSION_HIJACKED"
        ),
    },
    "Ransomware C2 Beacon": {
        "description": "🚨 Command & Control (C2): An infected company computer secretly messaging a hacker server right before a ransomware lockdown.",
        "logs": (
            "14:10:05 | WARNING  | IP: 10.0.0.87      | Connecting: hacker_server.io/c2 | Status: Periodic Ping Sent (Interval: 30s)\n"
            "14:10:35 | WARNING  | IP: 10.0.0.87      | Downloading: encrypted_tasks.bin| Status: Executing Remote Hacker Commands\n"
            "14:11:05 | WARNING  | IP: 10.0.0.87      | Connecting: hacker_server.io/c2 | Status: Alive Signal Confirmed\n"
            "14:11:35 | CRITICAL | IP: 10.0.0.87      | Action: Mass File Encryption    | Status: LOCKDOWN_TRIGGERED (204 KB sent)"
        ),
    },
}