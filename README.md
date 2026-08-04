# Automated-curtain-IoT-Project-Security-Evaluation

This is an IoT curtain controller built on a Raspberry Pi. Vulnerabilities of the system have been identified, exploited and remediated, with each fix verified by re-running the exploit.

## Overview:
The project started as an automated curtain system where a Raspberry Pi controls a motor via a Flask web server, including a scheduler which opens the curtains at sunrise and closes them at sunset. Just like any device on a network, there were security considerations to make during development, so I ran a full security lifecycle assessment on the system.

1. Threat Model -> Using OWASP and STRIDE, I defined 7 security goals and identified the attack surface of the system across the network and application layers.
2. Offensive assessment -> I carried out 7 attacks against the system, ranging from network reconnaissance to Denial-of-Service.
3. Remediation -> I implemented fixes/mitigations for the discovered vulnerabilities.
4. Verification -> Each attack was repeated but against the fixed system to verify the fixes worked.
5. Gap analysis -> I wrote a gap analysis which evaluates the current security posture of the system against the goals I defined in the threat model. It includes goals that were met or partially met and future work to be done.

> NOTE: All testing was done on my own hardware on my own network.

## System Overview:

<img width="3024" height="4032" alt="final build on window" src="https://github.com/user-attachments/assets/1288e006-c49f-46c5-b1e5-75726f6834e9" />

> The finished device on my window

### Hardware:
- Raspberry Pi 4 Model B
- 12V DC motor
- 12V 5A power supply
- BTS7960 H-bridge Driver
- Corded curtain rail
- 6mm Flange Coupling
- Solderless Breadboard Kit

### Software:
- Flask development web server with a mobile-friendly interface.
- Multiple different endpoints on the server tied to a specific operation (for example: open, close, stop, manual, auto).
- A scheduler which retrieves information about the time of sunset/sunrise for my location from the Sunrise-Sunset API and controls the curtains accordingly when in automatic mode.
- The application is implemented as a systemd service so it runs when the Raspberry Pi boots and runs without needing to be connected to the Pi from my laptop.

## Threat Model

Before testing, I needed to define 7 security goals for the system to achieve and identify the attack surface of the system across the network and application layers. I did this by writing a threat model document using OWASP and STRIDE.


| # | Security Goal | Requirement |
|---|---------------|-------------|
| 1 | Authentication | All inputs and commands must be authenticated to verify the identity of the person behind them |
| 2 | Confidentiality | All communications must be encrypted and unreadable to unauthorised entities |
| 3 | Integrity | All communications must have protection against tampering |
| 4 | Availability | The system should be protected against DoS attacks using rate-limiting and input validation |
| 5 | Non-Repudiation | The system should log all inputs and commands to keep a record of actions |
| 6 | Hardening | The Raspberry Pi should be hardened against compromise by removing unnecessary software and services |
| 7 | Secure Storage | Stored data should be held securely |


After the remediation phase, I compared where the system was against the goals I wanted to achieve in a gap analysis document (the risk rating found that Spoofing and Information Disclosure was the highest risk, caused by no authentication and unencrypted traffic): [Gap Analysis](Docs/Gap_Analysis.md)


Threat Model: [Threat Model](Docs/Threat_Model.md)

## My Findings:

| # | Attack | Tools | Finding | Goal Affected |
|---|--------|-------|---------|---------------|
| 1 | Network reconnaissance | Nmap | The Raspberry Pi was discoverable on the local network; port 5000 was open with the Flask development server and its version disclosed. | Hardening |
| 2 | Directory enumeration | Gobuster | All five endpoints of the web server were discovered without the need for credentials. | Authentication |
| 3 | Traffic analysis | tcpdump, Wireshark | Commands travelled in plaintext and were fully readable to anyone on the network listening to traffic. | Confidentiality |
| 4 | Unauthenticated access | curl | A single request to /open opened the curtain with no credentials or session needed. | Authentication |
| 5 | Replay | curl | A captured request could be replayed indefinitely; nothing in it was unique or time-bound, such as a nonce. | Authentication, Integrity |
| 6 | Cross-Site Request Forgery | Custom HTML page | A victim on the home network unknowingly sent the command from their own browser silently when the page was opened. | Authentication |
| 7 | Denial of Service | ApacheBench | No rate-limiting was implemented so an attacker could send as many requests as they wanted, on a development server that isn't designed to handle a high load. | Availability |
| - | Man-in-the-middle (ARP spoofing) | bettercap | **Unsuccessful** — it was blocked by my router's ARP protection features, not by any control on the device. | Confidentiality, Integrity |

## Remediations:

Each of my findings was fixed/mitigated and then they were verified to confirm the attacks no longer work on the system.

| Finding | Fix | Verification |
|---------|-----|--------------|
| Unauthenticated access, replay, CSRF | Session-based login authentication. Every control route is now protected by @require_login decorator. Passwords are stored as a Werkzeug scrypt hash. | I used curl to send a command to /open again and now a 302 redirect to /login is returned instead of an operation against the curtain. |
| Unencrypted Traffic | I implemented TLS/HTTPS using ssl_context. I also marked the session cookies as Secure so they're only ever sent over an encrypted channel. | I captured traffic using tcpdump again; the commands and http stream that were previously readable in Wireshark are now encrypted, and the http filter doesn't return anything. |
| CSRF | I hardened the session cookies by setting SameSite to Strict and adding the HttpOnly flag; this means that the browser will not attach the cookie to cross-site requests. | I tried to open the malicious page again and the request was rejected and the curtain didn't move. |
| No rate-limiting | I used Flask-Limiter to only allow 30 requests per minute per IP. | Sending over 100 requests started with 302 codes and after 30 requests it transitioned to 429 (Too Many Requests) codes. |
| No logging | I used Python's logging module and made it so that every command and login attempt was recorded with a timestamp and the source IP address. | The log file (curtain.log) shows the full audit trail, including failed login attempts and where they came from. |
| Least Privilege | I set up the application as a systemd service with the user set as ksiddy; this means that the app always runs as that user and never on root. | I used the command systemctl status curtain.service to verify where the service was running from. |

## Repository Structure

```
├── Code/
│   ├── app.py
│   ├── curtain.py
│   ├── motor.py
│   ├── sunset_api.py
│   └── config_reader.py
├── Diagrams/
│   ├── Diagram of Electrical Wiring.jpg
│   ├── Diagram of Mechanical Drive Assembly.jpg
│   └── Diagram of System Overview Pre-Implementation.jpg
├── Docs/
│   ├── Threat_Model.md
│   ├── Gap_Analysis.md
│   └── Requirement_Specification.md
└── README.md
```

## Limitations & Next Steps:

To preface, this was a home project using hardware I own. The following are the gaps between this home system and a full production system:

- The application runs on Flask's development server. The next step is to implement a production server (Gunicorn/Nginx).
- The certificates are self-signed. The next step is to get and use CA-signed certificates.
- The Raspberry Pi hasn't been hardened by removing unnecessary services and closing unused open ports yet.
- There is no input validation yet.
- Logs are stored locally. The next step would be to keep the logs in a tamper-resistant storage medium.
- There is a single password being shared for the web server. The next step would be to allow for multiple accounts for each user.
- The replay attack has been mitigated rather than fully eliminated. The next step would be to add a unique identifier to each request such as a nonce.
