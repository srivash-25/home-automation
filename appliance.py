"""
Generic Appliance Controller
Manages household appliances via relay modules.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

APPLIANCES = ["ac", "fan", "washing_machine", "microwave", "tv", "water_heater"]


class ApplianceController:
    def __init__(self, mqtt_client):
        self.mqtt       = mqtt_client
        self.appliances = {
            name: {"state": False, "last_changed": None, "total_on_minutes": 0}
            for name in APPLIANCES
        }
        self._on_since = {}

    def turn_on(self, appliance: str):
        if appliance not in self.appliances:
            return False
        self.appliances[appliance]["state"]        = True
        self.appliances[appliance]["last_changed"] = datetime.now().isoformat()
        self._on_since[appliance]                  = datetime.now()
        self.mqtt.control_appliance(appliance, True)
        logger.info(f"⚡ {appliance} ON")
        return True

    def turn_off(self, appliance: str):
        if appliance not in self.appliances:
            return False
        self.appliances[appliance]["state"]        = False
        self.appliances[appliance]["last_changed"] = datetime.now().isoformat()
        if appliance in self._on_since:
            delta = (datetime.now() - self._on_since.pop(appliance)).seconds // 60
            self.appliances[appliance]["total_on_minutes"] += delta
        self.mqtt.control_appliance(appliance, False)
        logger.info(f"⚡ {appliance} OFF")
        return True

    def get_status(self) -> dict:
        return self.appliances
