#include <WiFi.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

WiFiServer server(5000);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Starting TCP server...");
  server.begin();

  Serial.println("Server listening on port 5000");
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