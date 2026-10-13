
#include <WiFi.h>
#include "Buzzer.h"

const char* ssid = "ESP32_WIFI";
const char* password = "12345678";

#define BUTTON_PIN 22
#define BUZZER_PIN 23
#define GREEN_LED 18
#define YELLOW_LED 19
#define RED_LED 21

void setLED(int ledPin) {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);

  if (ledPin == GREEN_LED || ledPin == YELLOW_LED || ledPin == RED_LED) {
    digitalWrite(ledPin, HIGH);
  }
}


WiFiServer server(5000);
Buzzer buzzer(BUZZER_PIN);

bool continuousBuzzer = false;

void setup() {
  Serial.begin(115200);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  buzzer.begin();

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
  // Check button continuously, even without a laptop connection
  if (continuousBuzzer && digitalRead(BUTTON_PIN) == LOW) {
    buzzer.Buzzer_function("BUZZER_OFF");
    continuousBuzzer = false;
    Serial.println("Button pressed - Buzzer OFF");
  }

  WiFiClient client = server.available();

  if (client) {
    Serial.println("Laptop connected!");
    client.setTimeout(50);

    while (client.connected()) {
      // Check button while connected
      if (continuousBuzzer && digitalRead(BUTTON_PIN) == LOW) {
        buzzer.Buzzer_function("BUZZER_OFF");
        continuousBuzzer = false;
        Serial.println("Button pressed - Buzzer OFF");
        setLED(GREEN_LED);
      }

      if (client.available()) {
        String message = client.readStringUntil('\n');
        message.trim();

        Serial.print("Received: ");
        Serial.println(message);

        if (message == "1") {
          continuousBuzzer = true;
          buzzer.Buzzer_function("BUZZER_ON");
          setLED(RED_LED);
        }
        else if (message == "2") {
          buzzer.Buzzer_function("BUZZER_BURST");
          if(continuousBuzzer == false)
          {
              setLED(YELLOW_LED);
          }
        }
        else if (message == "3") {
          buzzer.Buzzer_function("BUZZER_BURST");
          if(continuousBuzzer == false)
          {
              setLED(YELLOW_LED);
          }
        }
        else
        {
            if(continuousBuzzer == false)
            {
              setLED(GREEN_LED);
            }
        }
        client.println("Message received by ESP32");

        Serial.print("Intensity: ");
        Serial.println(buzzer.getIntensity());
      }

      delay(5);
    }

    client.stop();
    Serial.println("Laptop disconnected");
    setLED(-1);
  }

  delay(5);
}



