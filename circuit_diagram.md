# Circuit Diagram & Wiring Guide

## ESP8266 (NodeMCU) — DHT22 + Relay

```
ESP8266 (NodeMCU)          DHT22 Sensor
┌─────────────┐            ┌─────────┐
│  3.3V  ──────────────────│  VCC    │
│  GND   ──────────────────│  GND    │
│  D4    ──────────────────│  DATA   │
└─────────────┘            └─────────┘

ESP8266 (NodeMCU)          4-Channel Relay Module
┌─────────────┐            ┌─────────────────┐
│  5V    ──────────────────│  VCC            │
│  GND   ──────────────────│  GND            │
│  D1    ──────────────────│  IN1 (Light 1)  │
│  D2    ──────────────────│  IN2 (Light 2)  │
│  D5    ──────────────────│  IN3 (Appliance)│
└─────────────┘            └─────────────────┘
```

## Arduino Uno — PIR Motion Sensor

```
Arduino Uno               PIR HC-SR501
┌──────────┐              ┌──────────┐
│  5V ──────────────────── VCC       │
│  GND ─────────────────── GND       │
│  D2  ─────────────────── OUT       │
└──────────┘              └──────────┘
```

## Smart Door Lock (Servo)

```
Arduino Uno               Servo Motor
┌──────────┐              ┌──────────┐
│  5V ──────────────────── VCC (red) │
│  GND ─────────────────── GND (blk) │
│  D9  ─────────────────── Signal(y) │
└──────────┘              └──────────┘
```

## Notes
- Use a 5V 2A power supply for the relay module; do NOT power relays from ESP8266 directly.
- Add a 10kΩ pull-up resistor between DHT22 DATA pin and VCC.
- For mains-powered appliances, use a qualified electrician for relay wiring.
