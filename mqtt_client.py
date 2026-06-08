"""
MQTT Client — handles all publish/subscribe communication
between the Python backend and IoT devices.
"""

import json
import logging
import paho.mqtt.client as mqtt
from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, TOPICS

logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self, client_id="home_automation_server"):
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect    = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message    = self._on_message
        self._callbacks = {}          # topic → list of handler functions

        if MQTT_USERNAME:
            self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self):
        """Connect to the MQTT broker and start the network loop."""
        self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        self.client.loop_start()
        logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")

    # ── Publish ───────────────────────────────────────────────────────────────

    def publish(self, topic: str, payload: dict, qos: int = 1):
        """Publish a JSON payload to a topic."""
        message = json.dumps(payload)
        result  = self.client.publish(topic, message, qos=qos)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logger.debug(f"Published → {topic}: {message}")
        else:
            logger.error(f"Failed to publish to {topic}, code={result.rc}")

    # ── Subscribe ─────────────────────────────────────────────────────────────

    def subscribe(self, topic: str, callback, qos: int = 1):
        """Subscribe to a topic and register a callback handler."""
        self.client.subscribe(topic, qos=qos)
        self._callbacks.setdefault(topic, []).append(callback)
        logger.info(f"Subscribed to {topic}")

    # ── Device Convenience Methods ────────────────────────────────────────────

    def control_light(self, room: str, state: bool, brightness: int = 100):
        self.publish(TOPICS["lighting"], {
            "room": room, "state": "ON" if state else "OFF",
            "brightness": brightness
        })

    def control_thermostat(self, target_temp: float, mode: str = "auto"):
        self.publish(TOPICS["thermostat"], {
            "target_temp": target_temp, "mode": mode
        })

    def control_door_lock(self, location: str, locked: bool):
        self.publish(TOPICS["door_lock"], {
            "location": location, "locked": locked
        })

    def control_appliance(self, name: str, state: bool):
        self.publish(TOPICS["appliance"], {
            "appliance": name, "state": "ON" if state else "OFF"
        })

    # ── Internal Callbacks ────────────────────────────────────────────────────

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("✅ MQTT connected successfully")
            # Re-subscribe on reconnect
            for topic in self._callbacks:
                client.subscribe(topic)
        else:
            logger.error(f"MQTT connection failed, return code={rc}")

    def _on_disconnect(self, client, userdata, rc):
        logger.warning(f"MQTT disconnected (rc={rc}). Auto-reconnect active.")

    def _on_message(self, client, userdata, msg):
        topic   = msg.topic
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except json.JSONDecodeError:
            payload = msg.payload.decode("utf-8")

        logger.debug(f"Received ← {topic}: {payload}")

        for registered_topic, handlers in self._callbacks.items():
            if mqtt.topic_matches_sub(registered_topic, topic):
                for handler in handlers:
                    try:
                        handler(topic, payload)
                    except Exception as e:
                        logger.error(f"Handler error on {topic}: {e}")
