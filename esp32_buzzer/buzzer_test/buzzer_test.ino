#include "Buzzer.h"

Buzzer buzzer(22);

void setup() {
  Serial.begin(115200);
  buzzer.begin();
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    buzzer.Buzzer_function(command);

    Serial.print("Command : ");
    Serial.println(command);
    Serial.print("Intensity: ");
    Serial.println(buzzer.getIntensity());
  }
}