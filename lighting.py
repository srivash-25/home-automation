"""
Lighting Control Module
Manages smart lights across all rooms.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

ROOMS = ["living_room", "bedroom", "kitchen", "bathroom", "entrance"]


class LightingController:
    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.lights = {
            room: {"state": False, "brightness": 100, "last_changed": None}
            for room in ROOMS
        }

    def turn_on(self, room: str, brightness: int = 100):
        if room not in self.lights:
            logger.warning(f"Unknown room: {room}")
            return False
        self.lights[room]["state"]        = True
        self.lights[room]["brightness"]   = brightness
        self.lights[room]["last_changed"] = datetime.now().isoformat()
        self.mqtt.control_light(room, True, brightness)
        logger.info(f"💡 Light ON — {room} @ {brightness}%")
        return True

    def turn_off(self, room: str):
        if room not in self.lights:
            return False
        self.lights[room]["state"]        = False
        self.lights[room]["last_changed"] = datetime.now().isoformat()
        self.mqtt.control_light(room, False)
        logger.info(f"💡 Light OFF — {room}")
        return True

    def set_brightness(self, room: str, brightness: int):
        brightness = max(0, min(100, brightness))
        if self.lights[room]["state"]:
            self.lights[room]["brightness"] = brightness
            self.mqtt.control_light(room, True, brightness)

    def turn_off_all(self):
        for room in ROOMS:
            self.turn_off(room)
        logger.info("All lights turned OFF")

    def get_status(self) -> dict:
        return self.lights
