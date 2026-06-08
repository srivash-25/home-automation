"""
Smart Door Lock Controller
Manages locking/unlocking with access logging.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DoorLock:
    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.locks = {
            "front_door": {"locked": True,  "last_action": None, "access_log": []},
            "back_door":  {"locked": True,  "last_action": None, "access_log": []},
            "garage":     {"locked": False, "last_action": None, "access_log": []},
        }

    def lock(self, location: str, user: str = "system"):
        if location not in self.locks:
            return False
        self.locks[location]["locked"]      = True
        self.locks[location]["last_action"] = datetime.now().isoformat()
        self._log(location, "LOCKED", user)
        self.mqtt.control_door_lock(location, locked=True)
        logger.info(f"🔒 {location} LOCKED by {user}")
        return True

    def unlock(self, location: str, user: str = "system"):
        if location not in self.locks:
            return False
        self.locks[location]["locked"]      = False
        self.locks[location]["last_action"] = datetime.now().isoformat()
        self._log(location, "UNLOCKED", user)
        self.mqtt.control_door_lock(location, locked=False)
        logger.info(f"🔓 {location} UNLOCKED by {user}")
        return True

    def lock_all(self):
        for location in self.locks:
            self.lock(location)

    def _log(self, location: str, action: str, user: str):
        entry = {"time": datetime.now().isoformat(), "action": action, "user": user}
        self.locks[location]["access_log"].append(entry)
        # Keep only last 50 entries
        self.locks[location]["access_log"] = self.locks[location]["access_log"][-50:]

    def get_status(self) -> dict:
        return self.locks
