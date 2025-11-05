#include <Arduino.h>

// Define stepper motor connections and steps per revolution:
#define DIR_PIN 14   // GPIO 18
#define STEP_PIN 12  // GPIO 19
#define STEPS_PER_REVOLUTION 200

void setup() {
  Serial.begin(115200);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
}

void loop() {
  Serial.println("Spinning clockwise slow");
  digitalWrite(DIR_PIN, HIGH);

  for (int i = 0; i < STEPS_PER_REVOLUTION; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(2000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(2000);
  }

  delay(1000);

  Serial.println("Spinning counterclockwise faster");
  digitalWrite(DIR_PIN, LOW);

  for (int i = 0; i < STEPS_PER_REVOLUTION; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);
  }

  delay(1000);

  Serial.println("Spinning clockwise fast");
  digitalWrite(DIR_PIN, HIGH);

  for (int i = 0; i < 5 * STEPS_PER_REVOLUTION; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500);
  }

  delay(1000);

  Serial.println("Spinning counterclockwise fast");
  digitalWrite(DIR_PIN, LOW);

  for (int i = 0; i < 5 * STEPS_PER_REVOLUTION; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(500);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(500);
  }

  delay(1000);
}
