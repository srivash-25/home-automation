"""
Home Automation Dashboard — Flask + SocketIO web application.
Serves the control UI and exposes a REST API for device control.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import logging
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from config.settings import SECRET_KEY, DEBUG, PORT, TOPICS
from src.communication.mqtt_client import MQTTClient
from src.devices.thermostat import Thermostat
from src.devices.lighting import LightingController
from src.devices.door_lock import DoorLock
from src.devices.appliance import ApplianceController
from src.automation.workflow_engine import WorkflowEngine
from src.automation.scheduler import Scheduler
from src.utils.energy_tracker import daily_report

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# ── Bootstrap devices ─────────────────────────────────────────────────────────
mqtt      = MQTTClient()
thermostat = Thermostat(mqtt)
lighting  = LightingController(mqtt)
door_lock = DoorLock(mqtt)
appliance = ApplianceController(mqtt)

devices  = {"lighting": lighting, "thermostat": thermostat,
             "door_lock": door_lock, "appliance": appliance}
workflow = WorkflowEngine(devices)
scheduler = Scheduler(workflow)

# ── MQTT message handlers ─────────────────────────────────────────────────────

def handle_thermostat_message(topic, payload):
    if "temperature" in payload:
        thermostat.update_reading(payload["temperature"],
                                  payload.get("humidity", 0))
        workflow.evaluate_sensor_trigger("temperature", payload["temperature"])
        socketio.emit("thermostat_update", thermostat.get_status())

mqtt.subscribe(TOPICS["thermostat"], handle_thermostat_message)
mqtt.subscribe(TOPICS["status"],
               lambda t, p: socketio.emit("device_status", p))

# ── REST API ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify({
        "thermostat": thermostat.get_status(),
        "lighting":   lighting.get_status(),
        "door_lock":  door_lock.get_status(),
        "appliance":  appliance.get_status(),
    })

@app.route("/api/lighting/<room>/<action>", methods=["POST"])
def api_lighting(room, action):
    brightness = request.json.get("brightness", 100) if request.is_json else 100
    ok = lighting.turn_on(room, brightness) if action == "on" else lighting.turn_off(room)
    socketio.emit("lighting_update", lighting.get_status())
    return jsonify({"success": ok, "status": lighting.get_status()})

@app.route("/api/door/<location>/<action>", methods=["POST"])
def api_door(location, action):
    ok = door_lock.unlock(location) if action == "unlock" else door_lock.lock(location)
    socketio.emit("door_update", door_lock.get_status())
    return jsonify({"success": ok, "status": door_lock.get_status()})

@app.route("/api/thermostat/set", methods=["POST"])
def api_thermostat_set():
    data   = request.get_json()
    target = float(data.get("target_temp", 22))
    mode   = data.get("mode", "auto")
    thermostat.set_target(target, mode)
    return jsonify({"success": True, "target": target, "mode": mode})

@app.route("/api/appliance/<name>/<action>", methods=["POST"])
def api_appliance(name, action):
    ok = appliance.turn_on(name) if action == "on" else appliance.turn_off(name)
    socketio.emit("appliance_update", appliance.get_status())
    return jsonify({"success": ok, "status": appliance.get_status()})

@app.route("/api/energy")
def api_energy():
    return jsonify(daily_report(appliance.get_status(), lighting.get_status()))

@app.route("/api/rules")
def api_rules():
    return jsonify(workflow.get_rules())

# ── Startup ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mqtt.connect()
    scheduler.start()
    print(f"🏠 Dashboard running at http://localhost:{PORT}")
    socketio.run(app, host="0.0.0.0", port=PORT, debug=DEBUG)
