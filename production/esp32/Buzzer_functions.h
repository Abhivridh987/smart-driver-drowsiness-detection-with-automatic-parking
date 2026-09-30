#ifndef BUZZER_FUNCTIONS_H
#define BUZZER_FUNCTIONS_H

class BuzzerFunctions {
  private:
    int buzzerPin;
    int intensity;

  public:
    BuzzerFunctions(int pin) {
      buzzerPin = pin;
      intensity = 255;
    }

    void begin() {
      ledcAttach(buzzerPin, 2000, 8);
      ledcWrite(buzzerPin, 0);
    }

    void on() {
      ledcWrite(buzzerPin, intensity);
    }

    void off() {
      ledcWrite(buzzerPin, 0);
    }

    void increase() {
      intensity += 25;
      if (intensity > 255)
        intensity = 255;

      ledcWrite(buzzerPin, intensity);
    }

    void reduce() {
      intensity -= 25;
      if (intensity < 0)
        intensity = 0;

      ledcWrite(buzzerPin, intensity);
    }

    void burst() {
      ledcWrite(buzzerPin, intensity);
      delay(1000);
      ledcWrite(buzzerPin, 0);
    }

    int getIntensity() {
      return intensity;
    }
};

#endif