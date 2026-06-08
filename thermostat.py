"""
Smart Thermostat Device Controller
Monitors temperature/humidity and controls heating/cooling.
"""

import logging
from datetime import datetime
from config.settings import TEMP_HIGH_THRESHOLD, TEMP_LOW_THRESHOLD

logger = logging.getLogger(__name__)


class Thermostat:
    def __init__(self, mqtt_client, device_id="thermostat_main"):
        self.mqtt      = mqtt_client
        self.device_id = device_id
        self.state = {
            "current_temp":    None,
            "current_humidity": None,
            "target_temp":     22.0,
            "mode":            "auto",   # auto | heat | cool | off
            "is_active":       False,
            "last_updated":    None,
        }

    def update_reading(self, temperature: float, humidity: float):
        """Called when sensor data arrives via MQTT."""
        self.state["current_temp"]     = temperature
        self.state["current_humidity"] = humidity
        self.state["last_updated"]     = datetime.now().isoformat()
        logger.info(f"Thermostat reading: {temperature}°C, {humidity}%RH")
        self._auto_regulate()

    def set_target(self, target_temp: float, mode: str = "auto"):
        self.state["target_temp"] = target_temp
        self.state["mode"]        = mode
        self.mqtt.control_thermostat(target_temp, mode)
        logger.info(f"Thermostat target set to {target_temp}°C ({mode} mode)")

    def _auto_regulate(self):
        if self.state["mode"] != "auto" or self.state["current_temp"] is None:
            return
        temp = self.state["current_temp"]
        if temp > TEMP_HIGH_THRESHOLD:
            self._activate("cool")
        elif temp < TEMP_LOW_THRESHOLD:
            self._activate("heat")
        else:
            self._deactivate()

    def _activate(self, mode: str):
        if not self.state["is_active"]:
            self.state["is_active"] = True
            logger.info(f"Auto-activating {mode} mode at {self.state['current_temp']}°C")
            self.mqtt.control_thermostat(self.state["target_temp"], mode)

    def _deactivate(self):
        if self.state["is_active"]:
            self.state["is_active"] = False
            logger.info("Temperature in range — deactivating thermostat")
            self.mqtt.control_thermostat(self.state["target_temp"], "off")

    def get_status(self) -> dict:
        return {**self.state, "device_id": self.device_id}
