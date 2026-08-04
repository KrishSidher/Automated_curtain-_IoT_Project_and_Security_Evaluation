# Threat Model:

## Introduction:
This Threat Model documents the potential security concerns behind my automated curtain IoT project.

### About the System:
The system uses a Raspberry-Pi connected to a remote device which acts as the controller over a local WiFi network. The remote device sends commands to the Raspberry-Pi either through manual intervention or the Raspberry-Pi will retrieve data about the local area's time of sunrise and sunset via an external API and operate the curtains accordingly. The use of a remote connection and the retrieval of data from a third party raises some security concerns which need to be evaluated through a security analysis.

### Approach:
We will be using the OWASP Threat Modelling approach, this will allow us to identify, quantify, and address the security risks associated with this system. Within this approach we will be using the STRIDE methodology, it was made by Microsoft and it classes threats into 6 categories:
- Spoofing -> related to Authentication.
- Tampering -> related to Integrity.
- Repudiation -> related to Non-Repudiation.
- Information Disclosure -> related to Confidentiality.
- Denial of Service -> related to Availability.
- Elevation of Privilege -> related to Authorisation.

## Scope and Objectives:

### Objectives:
- Identify potential security issues with the system.
- Assess the risks of each identified threat.
- Provide mitigations to these threats.
- Define security goals to facilitate gap analysis and evaluation of the finished implementation once the project is complete.

### In the Scope (what this threat model covers):
- The remote connection between the controller and the Raspberry-Pi over the local WiFi network.
- The connection between the Raspberry-Pi and the external API over the internet.
- The Raspberry-Pi itself.

### Out of Scope (what this threat model omits):
- Physical attacks directly on the hardware of the system.
- Integrations with smart-home platforms such as Amazon Alexa or Google Home.
- Attacks directed towards the client's device or the local WiFi network.

## System Decomposition:
Below is a DFD diagram which breaks down the system into its components, the flow of data and the trust boundaries. This allows us to analyse each element of the diagram using STRIDE.

### Figure 1: Data Flow Diagram
<img width="1351" height="1081" alt="DFD FINAL" src="https://github.com/user-attachments/assets/1bc2dcc4-096c-4fdf-af8d-3fe0919d60b7" />

### Components:
- Client's device (controller) -> This will be the client's device on which they can send commands to the Raspberry-Pi over the local network.
- Sunrise/Sunset API -> This is a third party service which will give data about the time of sunrise/sunset in the client's local area.
- Configuration Store -> This store is within the Raspberry-Pi and will store config details such as setting and credentials. The curtain control application will be able to read/write to it.

### Processes:
- Application for curtain control -> This software is on the Raspberry-Pi and it receives commands from the client's device and receives sunrise/sunset data from the external API. This will cause electrical signals to be sent to the motor which operates the opening/closing of the curtains.

### Data Flows:
- The client's device sends commands (such as open, close or stop the curtain) to the Raspberry-Pi's curtain control application remotely over the local network.
- The Raspberry-Pi's curtain control application returns status information to the client's device remotely over the local network.
- The Raspberry-Pi's curtain control application requests and receives data about the sunrise/sunset in the client's local area from an external API over the internet.
- The Raspberry-Pi's curtain control application reads from and writes to the configuration store.
- The Raspberry-Pi's curtain control application sends electrical signals to the motor to control it.

### Trust Boundaries:
- Boundary 1 -> This boundary encapsulates the local WiFi network where commands are sent between the client's device and Raspberry-Pi over it. Over the WiFi network any device can be a potential threat, so this boundary can't be completely trusted.
- Boundary 2 -> This boundary encapsulates the internet where sunrise/sunset information and requests for it are being sent between the external API and the Raspberry-Pi. This data is outside our zone of control so has to be treated as untrusted. We must therefore implement data validation.

## Threat Identification (STRIDE):
### Figure 2: STRIDE Table
<img width="820" height="5888" alt="STRIDE FINAL FINAL;" src="https://github.com/user-attachments/assets/e5028087-e6ab-47f7-9253-ea737e1af827" />

NOTE: After reviewing the STRIDE table above i've noticed the majority of security concerns arise from the same things, such as: no authentication, no/weak encryption, the absence of logging, no input validation and no rate-limiting. Addressing these issues will mitigate the majority of threats towards this system.

## Risk Assessment:
Each risk is rated by the likelihood of it happening and the impact it would have if it did occur. These 2 are then combined using a risk matrix to provide an overall risk rating.

### Figure 3: Risk Matrix
<img width="1143" height="365" alt="RISK MATRIX DONE" src="https://github.com/user-attachments/assets/bf0493f1-ad7e-47be-9a93-e060141e9bc1" />

### Figure 4: Risk Ratings
<img width="1133" height="5678" alt="RISK TABLE DONE" src="https://github.com/user-attachments/assets/6f4107ad-680c-4670-9fcd-83ed67f379cd" />

I've found the highest risks are: Spoofing and Information Disclosure at both the curtain control application and on the data flow between the application and the client's device. The majority of issues stem from: a lack in authentication and a lack in encryption of data in-transit. Therefore, we must put more resources towards mitigating these issues.

## Mitigations:

### Figure 5: Mitigations Table
<img width="820" height="3498" alt="MITIGATIONS TABLE FINAL" src="https://github.com/user-attachments/assets/e2c18310-6c30-48b6-b4f8-30b2205db1ae" />

A couple mitigations cover a wide range of threats here: TLS Encryption for tampering and information disclosure over data channels, authentication for spoofing, logging for repudiation. This reflects the pattern we saw during the risk rating process.

## Security Goals and Validation

### Security Goals:
- Authentication -> All inputs and commands into the system must be authenticated to verify the identity of the person behind them.
- Confidentiality -> All communications in the system must be encrypted and unreadable to unauthorised entities.
- Integrity -> All communications must have protection against tampering.
- Availability -> The system should be available and have protection against DoS attacks using rate-limiting and input validation.
- Non-Repudiation -> The system should log all inputs and commands to keep a record of actions done.
- Hardening -> The Raspberry-Pi should be hardened to prevent compromise, by removing unnecessary software and services.
- Secure Storage -> The storage of data should be secure (such as in the configuration store).

### Validation:
- Demonstrate the vulnerabilities in real-time -> We will confirm that these vulnerabilities actually exist by exploiting them to see if the prototype system meets our security goals or not.
- Mitigate vulnerabilities -> if there are exploits that are found we will mitigate them using the methods defined in our mitigations table.
- Test for vulnerabilities after mitigating threats -> We're going to repeat the same exploits we used initially to see if our mitigations were successful.
- Gap analysis -> We will conduct a comparison between where we are in terms of security posture compared to our goals and where we want to be to identify any risks that are left.

### Risks that will remain after validation:
There are some risks that are out of the scope of this project to mitigate, for example:
- Physical Attacks which interact with the hardware of the system.
- Attacks on the external API used.
- Attacks on the WiFi network used.
































