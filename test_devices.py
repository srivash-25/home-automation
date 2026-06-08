"""
Unit tests for device controllers.
Run: pytest tests/
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import unittest
from unittest.mock import MagicMock, patch
from src.devices.lighting import LightingController
from src.devices.door_lock import DoorLock
from src.devices.appliance import ApplianceController
from src.devices.thermostat import Thermostat


class TestLighting(unittest.TestCase):
    def setUp(self):
        self.mqtt = MagicMock()
        self.ctrl = LightingController(self.mqtt)

    def test_turn_on(self):
        result = self.ctrl.turn_on("living_room", 80)
        self.assertTrue(result)
        self.assertTrue(self.ctrl.lights["living_room"]["state"])
        self.assertEqual(self.ctrl.lights["living_room"]["brightness"], 80)

    def test_turn_off(self):
        self.ctrl.turn_on("bedroom")
        self.ctrl.turn_off("bedroom")
        self.assertFalse(self.ctrl.lights["bedroom"]["state"])

    def test_unknown_room(self):
        result = self.ctrl.turn_on("dungeon")
        self.assertFalse(result)

    def test_turn_off_all(self):
        for room in ["living_room", "bedroom", "kitchen"]:
            self.ctrl.turn_on(room)
        self.ctrl.turn_off_all()
        for room in self.ctrl.lights:
            self.assertFalse(self.ctrl.lights[room]["state"])


class TestDoorLock(unittest.TestCase):
    def setUp(self):
        self.mqtt = MagicMock()
        self.lock = DoorLock(self.mqtt)

    def test_initial_state(self):
        self.assertTrue(self.lock.locks["front_door"]["locked"])

    def test_unlock(self):
        self.lock.unlock("front_door", user="owner")
        self.assertFalse(self.lock.locks["front_door"]["locked"])

    def test_access_log(self):
        self.lock.unlock("front_door", user="test_user")
        log = self.lock.locks["front_door"]["access_log"]
        self.assertEqual(log[-1]["user"], "test_user")
        self.assertEqual(log[-1]["action"], "UNLOCKED")


class TestThermostat(unittest.TestCase):
    def setUp(self):
        self.mqtt = MagicMock()
        self.therm = Thermostat(self.mqtt)

    def test_update_reading(self):
        self.therm.update_reading(25.0, 60.0)
        self.assertEqual(self.therm.state["current_temp"], 25.0)

    def test_auto_cool_triggered(self):
        self.therm.update_reading(30.0, 55.0)   # > 28°C threshold
        self.assertTrue(self.therm.state["is_active"])

    def test_set_target(self):
        self.therm.set_target(24.0, "heat")
        self.assertEqual(self.therm.state["target_temp"], 24.0)
        self.mqtt.control_thermostat.assert_called_once_with(24.0, "heat")


if __name__ == "__main__":
    unittest.main()
