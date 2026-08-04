# Requirements Specification:

## Introduction:
This document names both the functional and non-functional requirements for my automated curtain project using a Raspberry-Pi. This system automates a set of curtains operated using a cord. This is done over my local network and therefore this IoT project is subject to a security analysis.

## Functional Requirements:
- FR1: The system will allow me to fully open and close the curtain when it received a command to do either.
- FR2: The system will keep the curtain in place when the curtains have reached their desired position.
- FR3: The system will be able to receive commands from a client's remote device over the local network via WiFi.
- FR4: The system will be able to open and close automatically based on the time of sunrise and sunset in the city (retrieved from an external source) the client is located in and with manual commands.
- FR5: The motor will be able to stop and continue operations on command to allow adjustments to the curtain.

## Non-Functional Requirements:
- N-FR1: Reliability -> The system will be able to open and close the curtain smoothly without the motor stalling or a mechanical failure occurring.
- N-FR2: Responsive -> The system will execute received instructions in a timely manner.
- N-FR3: Power -> The Raspberry-Pi will be powered using a USB-C power supply and the motor's power will separately be supplied by a battery pack.
- N-FR4: Usability -> The system will be able to be controlled using common household devices such as a mobile phone or laptop.
- N-FR5: Security -> The wireless communication between the system and controller will be protected against interception and unauthorised access.
- N-FR6: Size -> The system will not be too large as to be an eyesore. 
- N-FR7: Availability -> The system should be available at all times to interact with and control via the remote device.
- N-FR8: Usability -> The controls used to control the system from the remote device should be easy-to-use.

## Constraints:
- Strictly motor-controlled -> The curtains can only be controlled using the system and not manually unless system is detached from the curtain due to the self-locking worm gears of the motor.
- Lightweight curtains must be used to minimise friction due to the torque limitations of the motor.
- Remote connection is over the local WiFi network.
- Limited space around window to apply system.

## Assumptions:
- The cord-operated curtain rails should be fully intact and functional.
- The local WiFi network is available to facilitate the remote connection between the Raspberry-Pi and the System.
- The remote device is on the same local network as the Raspberry-Pi.
- The curtains slide smoothly over the railing with minimal friction.
- Information provided about the time of sunrise and sunset in the client's local area is accurate and reliable.

## Out of Scope:
- Remote access to the Raspberry-Pi from outside the local WiFi network.
- Manual Control of the cord-operated curtain rails.
- Integration with smart-home platforms such as Amazon Alexa or Google Home.
