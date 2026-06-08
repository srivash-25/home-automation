"""
Energy Tracker — estimates power usage per appliance.
"""

from datetime import datetime

# Approximate wattage per device (W)
WATTAGE = {
    "ac":             1500,
    "fan":              75,
    "washing_machine": 500,
    "microwave":       900,
    "tv":              100,
    "water_heater":   2000,
    "living_room":     60,   # lighting
    "bedroom":         40,
    "kitchen":         60,
    "bathroom":        20,
    "entrance":        20,
}


def estimate_kwh(device: str, on_minutes: float) -> float:
    watts = WATTAGE.get(device, 50)
    return round((watts * on_minutes / 60) / 1000, 4)


def daily_report(appliance_status: dict, lighting_status: dict) -> dict:
    report = {}
    for name, data in appliance_status.items():
        mins = data.get("total_on_minutes", 0)
        report[name] = {"on_minutes": mins, "kwh": estimate_kwh(name, mins)}
    for room, data in lighting_status.items():
        mins = 0   # would be tracked in a production system
        report[f"light_{room}"] = {"on_minutes": mins, "kwh": estimate_kwh(room, mins)}
    total = sum(v["kwh"] for v in report.values())
    return {"devices": report, "total_kwh": round(total, 4),
            "generated_at": datetime.now().isoformat()}
