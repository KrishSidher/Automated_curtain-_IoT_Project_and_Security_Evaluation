# Gap Analysis:

### Introduction:

This gap analysis document evaluates the security posture of my IoT curtain system. the remediation phase of the project is complete; this document compares what level of security I aimed for versus the level I achieved.

### Security Goals:

- Authentication -> Met using a Session-Based Login and hashing for the password.
- Confidentiality -> Met using TLS / HTTPS.
- Integrity -> Met using TLS (integrity in-transit) and signed session cookies.
- Availability -> Partially Met using rate-limiting. Input validation and using a production server via Gunicorn/Nginx would be the next step in fully meeting this goal.
- Non-Repudiation -> Met using logging.
- Hardening -> Partially met since the application is designed as a systemd service running on a non-root user (ksiddy). Using a production server, disabling unnecessary services and closing unused ports would be the next step in fully meeting this goal.
- Secure Storage -> Partially met using hashing for the user's password, hiding other secrets such as API keys and the hash itself from the source code would be the next step in meeting this goal.

### Security Goals in Detail:

#### Authentication (Met):

- Implemented Session-Based Login Authentication. Different directory routes (/open, /close, /stop, /manual, /auto) and the home page are protected behind a login page (/login) which will reject any unauthenticated requests and instead redirect them to the login page. The password is hashed using a scrypt password hash.
  
- I verified this by running a curl replay attack to try and control the system while on the local network. After implementing authentication a 302 redirect message is returned. This prevents the Replay and CSRF attack demonstrated.
  
- Notes: A single password is shared among everyone rather than individual credentials/accounts. A production system would opt for individual accounts, however since only I would be using the system I did not implement this. Also, replay attacks are mitigated rather than eliminated: TLS prevents the capture of commands nad the requirement of a session prevents unauthenticated requests, but there is no unique identifier between requests such as a nonce, so a valid session once obtained could be reused. The next step would be to add request uniqueness.

#### Confidentiality (Met):

- Implemented TLS/HTTPS using ssl_context configurations and session cookies are marked as "Secure" so they're only sent over an encrypted channel.
  
- I verified this by capturing traffic over wlan0 using tcpdump and analysing the file on Wireshark. Previously exposed http commands shown in plaintext are now encrypted and unreadable.
  
- Notes: The TLS certificate is self-signed, and therefore does not provide third-party verification. For future work I must implement a CA signed certificate (for example from 'Let's Encrypt').

#### Integrity (Met):

- Implemented using TLS (TLS ensures that messages in-transit haven't been altered, lost or corrupted). Also, Flask signs the cookie which holds the session state, meaning the cookie holding information as to whether or not you are logged in is signed using a secret key held on the server and nowhere else, meaning that a logged-in state cannot be forged/modified despite the cookie living within the client's browser.

- TLS was verified in Goal 2 (Confidentiality)

- Notes: For a future build integrity checks at the application layer would be an addition which facilitates defence in-depth.

#### Availability (Partially Met):

- Implemented using rate-limiting using the Flask-limiter library which is configured to only allow 30 requests per minute per IP address.

- I verified this by running a flood of requests to the home page and saw a transition of HTTP status codes from 302 (redirect to /login) to 429 (Too many requests) after 30 requests were sent. Any requests after those initial 30 are refused.

- Notes: The next step is adding input validation and using a production server where Nginx can buffer responses for slower clients to protect Gunicorn from DOS attacks.

#### Non-Repudiation (Met):

- I implemented Application Logging using Python's logging module. Every command is recorded with a timestamp and the source IP address, this includes both successful and failed login attempts.

- I verified this by looking at my 'curtain.log' file after inputting a valid and invalid password, and I saw the recorded series of events including what happened and where it came from.

- Notes: The logs are shown in plaintext in the log file on the Raspberry Pi, the next step would be implementing a tamper-resistant method of storing logs.

#### Hardening (Partially Met):

- I implemented the application the web application runs on as a systemd service running as a non-root user (ksiddy). This is important so that if the application is compromised the attacker doesn't have root access to the Raspberry Pi.

- I verified this by using the command systemctl status curtain.service to verify that the service is running as a non-root user.

- Notes: The next step would be to disable unnecessary services, close open ports that aren't necessary, and use a production server to reduce the attack surface of the system.

#### Secure Storage (Partially Met): 

- The user's password is stored as a salted scrypt hash.

- Notes: Other pieces of sensitive information such as the secret key and the password hash are currently held in the source code for the web application, the next step would be moving these secrets to a secure location.

### Conclusion:

- Out of the 7 security goals, 4 of them were fully met and 3 were partially met with defined steps to improve them in the future. I checked that each of these controls were working by repeating the attacks I demonstrated before the remediation phase, and confirmed they no longer succeed.

- The remaining work to be done primarily is concentrated around the production server used, a CA signed certificate, OS hardening and input validation. These steps will help turn this system from a secure prototype to a production-level system.











