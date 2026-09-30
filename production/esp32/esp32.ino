#include <WiFi.h>
#include "Buzzer.h"


const char* ssid = "ESP32_WIFI";
const char* password = "12345678";

WiFiServer server(5000);
Buzzer buzzer(22);

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
  buzzer.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Laptop connected!");

    while (client.connected()) {

      if (client.available()) {

        String message = client.readStringUntil('\n');
        Serial.print("Received: ");
        Serial.println(message);

        message.trim();
        
        if (message == "1"){
            buzzer.Buzzer_function("BUZZER_BURST");
        }
        else if (message == "2"){
            buzzer.Buzzer_function("BUZZER_BURST");
        }
        else if ( message == "3") {
            buzzer.Buzzer_function("BUZZER_BURST");
        }
        

        client.println("Message received by ESP32");
        Serial.print("Intensity: ");
        Serial.println(buzzer.getIntensity());
      }
    }

    client.stop();

    Serial.println("Laptop disconnected");
  }
}