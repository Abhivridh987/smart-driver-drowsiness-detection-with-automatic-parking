#include <WiFi.h>

const char* ssid = "ESP32_WIFI";
const char* password = "12345678";

WiFiServer server(5000);

void setup() {
  Serial.begin(115200);

  WiFi.softAP(ssid, password);

  Serial.println();
  Serial.println("ESP32 WiFi started");

  Serial.print("WiFi Name: ");
  Serial.println(ssid);

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.softAPIP());

  server.begin();

  Serial.println("TCP server started");
  Serial.println("Listening on port 5000");
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Laptop connected!");

    while (client.connected()) {
      if (client.available()) {
        String message = client.readString();

        Serial.print("Received: ");
        Serial.println(message);

        client.println("Message received by ESP32");

        break;
      }
    }

    client.stop();
    Serial.println("Laptop disconnected");
  }
}