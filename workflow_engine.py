"""
Automation Workflow Engine
Evaluates trigger-action rules to automate the smart home.
"""

import json
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)


class WorkflowEngine:
    def __init__(self, devices: dict):
        """
        devices: {
            "lighting":  LightingController instance,
            "thermostat": Thermostat instance,
            "door_lock":  DoorLock instance,
            "appliance":  ApplianceController instance,
        }
        """
        self.devices = devices
        self.rules   = self._load_default_rules()

    def _load_default_rules(self):
        """Built-in automation rules (can be extended via rules.json)."""
        return [
            {
                "id":       "night_lock",
                "name":     "Lock all doors at 10 PM",
                "trigger":  {"type": "time", "at": "22:00"},
                "action":   {"device": "door_lock", "method": "lock_all"},
                "enabled":  True,
            },
            {
                "id":       "night_dim",
                "name":     "Dim lights at 10 PM",
                "trigger":  {"type": "time", "at": "22:00"},
                "action":   {"device": "lighting", "method": "set_brightness",
                             "params": {"room": "living_room", "brightness": 20}},
                "enabled":  True,
            },
            {
                "id":       "morning_unlock",
                "name":     "Unlock front door at 6 AM",
                "trigger":  {"type": "time", "at": "06:00"},
                "action":   {"device": "door_lock", "method": "unlock",
                             "params": {"location": "front_door"}},
                "enabled":  True,
            },
            {
                "id":       "high_temp_ac",
                "name":     "Turn on AC when temperature > 28°C",
                "trigger":  {"type": "sensor", "sensor": "temperature",
                             "condition": "gt", "value": 28},
                "action":   {"device": "appliance", "method": "turn_on",
                             "params": {"appliance": "ac"}},
                "enabled":  True,
            },
        ]

    def evaluate_time_triggers(self):
        """Call this every minute from the scheduler."""
        now_str = datetime.now().strftime("%H:%M")
        for rule in self.rules:
            if not rule["enabled"]:
                continue
            trigger = rule["trigger"]
            if trigger["type"] == "time" and trigger.get("at") == now_str:
                logger.info(f"⏰ Firing rule: {rule['name']}")
                self._execute(rule["action"])

    def evaluate_sensor_trigger(self, sensor: str, value: float):
        """Call this when a sensor reading changes."""
        for rule in self.rules:
            if not rule["enabled"]:
                continue
            trigger = rule["trigger"]
            if trigger["type"] != "sensor" or trigger.get("sensor") != sensor:
                continue
            threshold = trigger["value"]
            condition = trigger["condition"]
            fired = (
                (condition == "gt" and value > threshold) or
                (condition == "lt" and value < threshold) or
                (condition == "eq" and value == threshold)
            )
            if fired:
                logger.info(f"🌡️ Sensor rule fired: {rule['name']} ({sensor}={value})")
                self._execute(rule["action"])

    def _execute(self, action: dict):
        device_key = action["device"]
        method     = action["method"]
        params     = action.get("params", {})
        device     = self.devices.get(device_key)
        if device is None:
            logger.error(f"Device '{device_key}' not found in registry")
            return
        func = getattr(device, method, None)
        if func is None:
            logger.error(f"Method '{method}' not found on {device_key}")
            return
        try:
            func(**params)
        except Exception as e:
            logger.error(f"Rule execution error ({method}): {e}")

    def add_rule(self, rule: dict):
        self.rules.append(rule)

    def get_rules(self):
        return self.rules
