# 🏠 Home Automation System — IoT-Based Smart Home Solution

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![MQTT](https://img.shields.io/badge/Protocol-MQTT-orange)
![IoT](https://img.shields.io/badge/IoT-ESP8266%2FArduino-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

> **Duration:** December 2023 – March 2024  
> An end-to-end IoT solution for monitoring and controlling smart home devices via a centralized dashboard with real-time communication, automation workflows, and energy optimization.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Hardware Components](#hardware-components)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Dashboard Preview](#dashboard-preview)
- [Automation Workflows](#automation-workflows)
- [Contributors](#contributors)

---

## Overview

This project implements a fully functional **Smart Home Automation System** that connects physical IoT devices (thermostats, lights, door locks, cameras, appliances) through MQTT protocol and provides a real-time web dashboard for remote monitoring and control.

---

## Features

- 🌡️ **Smart Thermostat** — Real-time temperature/humidity monitoring and automated regulation
- 💡 **Lighting Control** — Remote on/off, dimming, and schedule-based automation
- 🔒 **Smart Door Locks** — Remote lock/unlock with access logging
- 📷 **Security Cameras** — Live feed monitoring and motion-triggered alerts
- 🏠 **Appliance Control** — Switch household devices on/off remotely
- 📊 **Centralized Dashboard** — Web-based UI for device monitoring and control
- ⚡ **Energy Optimization** — Intelligent scheduling to reduce power consumption
- 🔔 **Real-Time Alerts** — MQTT-based notifications on device state changes
- 🔁 **Automation Workflows** — Trigger-action rules (e.g., lock doors at night, dim lights at sunset)

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Web Dashboard (Flask)               │
│          Remote Monitoring & Control UI              │
└────────────────────┬────────────────────────────────┘
                     │ HTTP / WebSocket
┌────────────────────▼────────────────────────────────┐
│              Python Backend Server                   │
│     Device Manager │ Automation Engine │ API         │
└────────────────────┬────────────────────────────────┘
                     │ MQTT Protocol
┌────────────────────▼────────────────────────────────┐
│               MQTT Broker (Mosquitto)                │
└──┬──────────┬──────────┬──────────┬─────────────────┘
   │          │          │          │
┌──▼──┐  ┌───▼──┐  ┌────▼─┐  ┌────▼──┐
│ESP  │  │Arduino│  │Temp  │  │Door   │
│8266 │  │Lights │  │Sensor│  │Lock   │
│WiFi │  │Relay  │  │DHT22 │  │Servo  │
└─────┘  └──────┘  └──────┘  └───────┘
```

---

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Language     | Python 3.9+                         |
| IoT Protocol | MQTT (via Mosquitto Broker)         |
| Microcontrollers | ESP8266, Arduino Uno/Nano       |
| Sensors      | DHT22, PIR, LDR, Ultrasonic         |
| Backend      | Flask, Flask-SocketIO               |
| Frontend     | HTML5, CSS3, JavaScript, Chart.js   |
| Communication | Wi-Fi (IEEE 802.11 b/g/n)         |
| Database     | SQLite (device logs & schedules)    |
| Embedded     | Arduino IDE, MicroPython            |

---

## Hardware Components

| Component         | Model / Module       | Purpose                        |
|------------------|----------------------|-------------------------------|
| Microcontroller  | ESP8266 (NodeMCU)    | Wi-Fi-enabled IoT node         |
| Microcontroller  | Arduino Uno/Nano     | Sensor reading & relay control |
| Temp/Humidity    | DHT22 Sensor         | Climate monitoring             |
| Motion Sensor    | PIR HC-SR501         | Security / automation trigger  |
| Light Sensor     | LDR Module           | Ambient light detection        |
| Relay Module     | 4-Channel 5V Relay   | Appliance & light switching    |
| Door Lock        | Servo Motor + Solenoid | Smart lock actuation         |
| Display          | OLED 0.96" (I2C)     | Local device status display    |
| Power Supply     | 5V/3.3V Adapter      | System power                   |

---

## Project Structure

```
home-automation/
├── src/
│   ├── devices/
│   │   ├── thermostat.py       # Thermostat device controller
│   │   ├── lighting.py         # Lighting control module
│   │   ├── door_lock.py        # Smart lock controller
│   │   ├── security_camera.py  # Camera monitoring module
│   │   └── appliance.py        # Generic appliance controller
│   ├── automation/
│   │   ├── workflow_engine.py  # Automation rule engine
│   │   ├── scheduler.py        # Device scheduling
│   │   └── rules.json          # Predefined automation rules
│   ├── communication/
│   │   ├── mqtt_client.py      # MQTT publish/subscribe handler
│   │   └── websocket_handler.py
│   └── utils/
│       ├── logger.py
│       └── energy_tracker.py
├── hardware/
│   ├── esp8266/
│   │   ├── esp8266_main.ino    # ESP8266 Arduino sketch
│   │   └── wifi_config.h
│   ├── arduino/
│   │   └── sensor_node.ino     # Arduino sensor node sketch
│   └── sensors/
│       └── dht22_reader.py
├── dashboard/
│   ├── app.py                  # Flask web application
│   ├── templates/
│   │   └── index.html          # Dashboard UI
│   └── static/
│       ├── style.css
│       └── dashboard.js
├── config/
│   └── settings.py             # Global configuration
├── tests/
│   ├── test_devices.py
│   └── test_automation.py
├── docs/
│   └── circuit_diagram.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- [Mosquitto MQTT Broker](https://mosquitto.org/download/)
- Arduino IDE (for hardware flashing)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/home-automation.git
cd home-automation
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your MQTT broker address, Wi-Fi credentials, etc.
```

### 4. Start the MQTT Broker
```bash
mosquitto -c /etc/mosquitto/mosquitto.conf
```

### 5. Flash Hardware
- Open `hardware/esp8266/esp8266_main.ino` in Arduino IDE
- Update Wi-Fi credentials in `wifi_config.h`
- Flash to ESP8266 board

---

## How to Run

```bash
# Start the backend + dashboard
python dashboard/app.py
```

Open your browser at `http://localhost:5000`

---

## Automation Workflows

| Trigger                   | Action                              |
|--------------------------|--------------------------------------|
| Time = 10:00 PM          | Lock all doors + dim lights to 20%  |
| Temperature > 28°C       | Turn on AC / Fan                    |
| Motion detected (night)  | Turn on security lights + alert     |
| Time = 6:00 AM           | Unlock door + raise thermostat      |
| No motion for 30 minutes | Turn off lights in that room        |

---

## Contributors

| Name | Role |
|------|------|
| [Your Name](https://github.com/YOUR_USERNAME) | Full-Stack IoT Developer |

---

## License

This project is licensed under the [MIT License](LICENSE).
