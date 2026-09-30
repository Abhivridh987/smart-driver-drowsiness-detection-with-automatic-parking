#ifndef BUZZER_H
#define BUZZER_H

#include "Buzzer_functions.h"

class Buzzer {
  private:
    BuzzerFunctions buzzer;

  public:
    Buzzer(int pin) : buzzer(pin) {
    }

    void begin() {
      buzzer.begin();
    }

    void Buzzer_function(String command) {
      if (command == "ON") {
        buzzer.on();
      }
      else if (command == "OFF") {
        buzzer.off();
      }
      else if (command == "BUZZER_INCREASE") {
        buzzer.increase();
      }
      else if (command == "BUZZER_DECREASE") {
        buzzer.reduce();
      }
      else if (command == "BUZZER_BURST"){
        buzzer.burst();
      }
    }

    int getIntensity() {
      return buzzer.getIntensity();
    }
};

#endif