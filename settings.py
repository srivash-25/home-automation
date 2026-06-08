import os
from dotenv import load_dotenv

load_dotenv()

# ── MQTT ──────────────────────────────────────
MQTT_BROKER   = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT     = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# ── MQTT Topics ───────────────────────────────
TOPICS = {
    "thermostat": "home/thermostat",
    "lighting":   "home/lighting",
    "door_lock":  "home/door_lock",
    "camera":     "home/camera",
    "appliance":  "home/appliance",
    "status":     "home/status",
}

# ── Flask ─────────────────────────────────────
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret")
DEBUG      = os.getenv("FLASK_DEBUG", "True") == "True"
PORT       = int(os.getenv("FLASK_PORT", 5000))

# ── Thresholds ────────────────────────────────
TEMP_HIGH_THRESHOLD = 28   # °C — trigger cooling
TEMP_LOW_THRESHOLD  = 18   # °C — trigger heating
MOTION_TIMEOUT_MIN  = 30   # minutes before auto-off
