/*
 * ESP8266 Smart Home Node
 * Reads DHT22 sensor and publishes to MQTT broker.
 * Subscribes to lighting/appliance topics to control relays.
 *
 * Libraries required (install via Arduino Library Manager):
 *   - PubSubClient by Nick O'Leary
 *   - DHT sensor library by Adafruit
 *   - ArduinoJson by Benoit Blanchon
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ── WiFi & MQTT — update these ──────────────────────────────────────────────
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* MQTT_BROKER   = "192.168.1.100";   // your server's local IP
const int   MQTT_PORT     = 1883;
const char* MQTT_USER     = "";
const char* MQTT_PASS     = "";

// ── Pins ─────────────────────────────────────────────────────────────────────
#define DHT_PIN   D4
#define RELAY_PIN D1      // controls light / appliance via relay module
#define DHT_TYPE  DHT22

DHT         dht(DHT_PIN, DHT_TYPE);
WiFiClient  wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL_MS = 10000;   // 10 s

// ── MQTT callback — incoming commands ────────────────────────────────────────
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<128> doc;
  deserializeJson(doc, payload, length);

  String topicStr = String(topic);

  if (topicStr == "home/lighting") {
    String state = doc["state"].as<String>();
    digitalWrite(RELAY_PIN, state == "ON" ? HIGH : LOW);
    Serial.println("Light → " + state);
  }
  if (topicStr == "home/appliance") {
    String state = doc["state"].as<String>();
    digitalWrite(RELAY_PIN, state == "ON" ? HIGH : LOW);
    Serial.println("Appliance → " + state);
  }
}

// ── WiFi Setup ────────────────────────────────────────────────────────────────
void setupWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
}

// ── MQTT Reconnect ────────────────────────────────────────────────────────────
void reconnectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    bool ok = strlen(MQTT_USER) > 0
                ? mqtt.connect("esp8266_node", MQTT_USER, MQTT_PASS)
                : mqtt.connect("esp8266_node");
    if (ok) {
      Serial.println("connected");
      mqtt.subscribe("home/lighting");
      mqtt.subscribe("home/appliance");
    } else {
      Serial.println("failed, retry in 5s");
      delay(5000);
    }
  }
}

// ── Setup & Loop ──────────────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  dht.begin();
  setupWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
}

void loop() {
  if (!mqtt.connected()) reconnectMQTT();
  mqtt.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;

    float temp = dht.readTemperature();
    float hum  = dht.readHumidity();

    if (!isnan(temp) && !isnan(hum)) {
      StaticJsonDocument<64> doc;
      doc["temperature"] = temp;
      doc["humidity"]    = hum;
      char buf[64];
      serializeJson(doc, buf);
      mqtt.publish("home/thermostat", buf);
      Serial.printf("Published: %.1f°C  %.1f%%\n", temp, hum);
    }
  }
}
